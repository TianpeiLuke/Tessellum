# Tessellum CLI (`src/tessellum/cli/`)

## The idea

Tessellum is a system in layers: a markdown vault you author, a SQLite index that answers questions about it, and a pair of LLM-backed runtimes that reason over it. The CLI is the single operator surface across all of them. Its governing idea is that it holds no knowledge of its own. Every command is a thin wrapper that parses flags, calls one runtime function, and turns the outcome into an exit code. The intelligence lives in the runtime packages; the CLI only frames the conversation with them.

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
   init, capture,            index build           search, filter,    composer,
   format check,             (vault → SQLite)      fz, bb audit        dks, mcp serve
   bb migrate                                      (read the DB)      (LLM / server)
```

The whole dispatcher is one convention: an attribute named `func` on the parsed arguments. Each command module contributes an `add_subparser` call that registers its own parser and binds its own handler with `set_defaults(func=...)`. `main` parses, finds `func`, calls it, and returns its integer exit code. There is no registry and no lookup table. A command definition and the code that runs it sit in the same file, and `main.py` stays a flat list of registrations.

The commands sort naturally by what they touch, and this is the mental map worth keeping. Some commands never leave the filesystem — they scaffold, capture, validate, or rewrite markdown, the write-side of the system. One command, `index build`, is the bridge from the vault to the index. A cluster of read commands — search, filter, and the Folgezettel and Building-Block explorers — only ever read that index back. And two commands are runtimes proper: the Composer executes typed pipelines, and DKS runs the dialectic cycle, both LLM-backed, with the MCP server standing alongside as a long-lived process. This is the CQRS split made visible on the command line: writing and reading are different verbs with different consequences.

Grouped commands nest a second layer of the same trick. `composer`, `index`, and `format` demand a sub-subcommand and let argparse error if it is missing. But `fz`, `bb`, and `mcp` also answer to their bare form — typing `tessellum fz` with no verb reaches a handler that prints its usage and exits. The difference is deliberate: an interactive explorer should tell you your options, whereas a required-leaf group should fail loudly.

## How work flows through it

A first session runs the layers in order. You scaffold a vault with `init`, which copies a seed structure into an empty (or, with `--force`, a non-empty) directory. You author notes with `capture`, each one stamped from a typed template chosen by flavor. You check them with `format check`, which validates YAML frontmatter against the closed-enum spec and, on a directory, recurses over every markdown file while skipping the obvious non-notes like `README.md` and `Rank_*`. Then `index build` reads the whole vault into a single SQLite database — notes, links, full-text, and, unless you pass `--no-dense`, vector embeddings.

Once the index exists, the read commands answer questions against it. `search` is the content surface, and its four strategies are a single mutually-exclusive choice with hybrid as the default: BM25 for lexical matching, dense for semantic similarity, hybrid fusing the two by reciprocal rank, and best-first BFS that walks the link graph outward from a seed note. That last one is the exception worth remembering — its query argument is not free text but a vault-relative note path. `filter`, by contrast, is metadata-only. It answers *what kind* of note you want — a status, a building block, a tag, a date range, a Folgezettel prefix — by filtering columns directly, and all its predicates AND together. The division is clean by design: content lives under `search`, structure under `filter`.

The Folgezettel explorer, `fz`, treats the trail structure as a query rather than a stored artifact. Tessellum keeps only two columns per note — a Folgezettel id and its parent — and derives every path, depth, and trail at query time by walking that parent chain in Python. Its verbs read like the questions you actually ask of a trail: list the trails, show a subtree, trace the ancestors from root to a node, expand its descendants, or print the full path with siblings. The walks are cycle-safe by construction, so a malformed parent link degrades gracefully instead of looping.

The `bb` command reports on the Building-Block graph. Its `audit` verb loads the corpus graph from the index and tallies the shape of the knowledge: how many nodes of each type, how many edges of each epistemic label, which edges the schema allows but the corpus has never realized, and which nodes float unconnected. Its `migrate` verb is a careful one — it walks the vault to find notes whose recorded schema version lags the current one and classifies each as would-pass or would-fail under today's rules. With `--apply` it advances the version stamp, but only on notes that would already pass validation. It never silently rewrites content that does not conform.

The two runtimes carry the real weight. `composer` runs a pipeline defined by a single self-contained skill canonical whose step sections each carry a typed contract block: `validate` checks those contract blocks against the spec, `compile` turns them into a typed DAG with zero LLM calls, and `run` executes that DAG against a set of leaves. `batch` runs many such jobs in parallel with resume, `eval` scores scenarios against assertions and an LLM-judge rubric, and `scaffold-sidecar` prints a starter contract block per section anchor for the author to paste into the canonical. `dks` drives the Dialectic Knowledge System — a multi-cycle run over a JSONL of observations, with report, calibration, and schema-mutating meta modes that short-circuit the observation run. And `mcp serve` re-exposes these same runtime APIs as MCP tools over stdio, so an agent host can call them the way a human calls the CLI.

## Design decisions and why

**Thin CLI over fat runtime.** Every handler does the same three things: translate flags into one runtime call, map the exceptions that call can raise onto exit codes, and format the result. It reimplements nothing. This is not a stylistic preference but the load-bearing invariant of the whole interface. Because the runtime is the single source of behaviour, the CLI, the MCP tools, and the test suite cannot disagree about what a command means.

**The exit code is a contract, not a courtesy.** Three codes carry a precise meaning across every command. Zero is success. One is a domain failure — a note that fails validation, a target that already exists, a skill that will not compile. Two is an invocation failure — a missing database, a missing dependency, a malformed argument. The split between one and two is the useful part: a script branches on it to know whether to fix the *content* or fix the *call*. That distinction is codified per module, not left to convention.

**`--format json` on every read and telemetry command.** The reader is often a machine — an agent, a CI job, the MCP layer — not a person. So each command that reports something offers a `human` view and a `json` view of the same data. One command serves both audiences without a second code path.

**The serial Composer path is the default and stays byte-identical.** `composer run` defaults to the serial reference executor. The wave-parallel dynamic scheduler is strictly opt-in behind `--dynamic`, and every flag that belongs to it — workers, manifest, close-gate, budgets, and the rest — is inert without that switch. The reason is trust: a faster runtime earns adoption only if it cannot silently change the reference semantics. Making the parallel path opt-in guarantees the default answer never moves.

**Gates never call an LLM, and neither does compilation.** `compile` produces a typed DAG with zero model calls, and the plan, session, and wave gates that guard the dynamic path are deterministic checks. Validation and structure are cheap, repeatable, and free of network flakiness; only execution spends tokens. Keeping the boundary sharp means the parts you run constantly stay fast and offline.

**DKS is a peer runtime, not a Composer subcommand.** The Dialectic Knowledge System reuses Composer's backend abstractions but lives at the top level as `tessellum dks`. It has its own lifecycle and its own mode surface — report, calibrate, meta — that has nothing to do with pipeline execution. Nesting it under `composer` would conflate two independent runtimes.

**Folgezettel topology is derived, not materialized.** There is no trail view in the schema. Trails are reconstructed in memory each time, because the vaults this targets are small — typically well under a thousand trail notes — and an in-memory walk is simpler and more portable than a recursive SQL query and needs no extra schema to maintain.

**Optional dependencies stay optional.** The MCP SDK, the Anthropic bridge, and the paper and ingest toolchains are all extras. None of them is imported at module load. Each is pulled in lazily at the exact call site that needs it, and a missing extra returns exit two with an install hint. The consequence is that the base CLI loads and runs even when nothing optional is installed — you never pay for a feature you are not using.

**Reference:** [reference/cli.md](reference/cli.md) — API, symbols, and signatures.
