# composer-ts — a thin TypeScript bridge over the Python Composer

`composer-ts` is a **control-flow bridge**, not a port. It gives the
Composer a TypeScript orchestration front-door for the TS-native agent
ecosystem (Claude Code and other TS agent runtimes / IDE agents) while the
Python substrate — the compiler, typed contracts, materializer, gates, the
unified vault DB, and the v4 wave scheduler — stays the **single source of
truth**.

## Doctrine: bridge, don't port

A full Python→TypeScript port was scoped and rejected as *feasible but not
worth it*: the ~25 person-week cost buys, at best, behavior-close
reproduction, and its one irreducible risk (embedding-fidelity drift from
`sentence-transformers` → transformers.js/ONNX) lands on retrieval — the
subsystem that defines the product's value. So the split is:

| Plane | Owns | Where |
|---|---|---|
| **TS (this package)** | control flow + DAG-walk ergonomics (ready-frontier, dependency columns) + invocation | `composer-ts/src/` |
| **Python substrate** | compile, typed-contract validation, materialize, gates, DB, the v4 `run_pipeline_dynamic` scheduler | `src/tessellum/` |

**The bridge holds ZERO contract logic.** It cannot become a second,
drifting authority because it never re-implements compilation or
validation — it shells the existing `tessellum composer` CLI over a
subprocess boundary and parses its JSON. Python re-validates every
artifact on ingest; a compile error surfaces as a `BridgeError`, never a
silent partial.

## No build toolchain, no dependencies

Runs under Node's native TypeScript type-stripping (Node ≥ 22.6 with
`--experimental-strip-types`; default on Node ≥ 23). Zero npm
dependencies — Node built-ins only (`node:child_process`, `node:test`).

## API

```ts
import { compile, run, columns, readyFrontier } from "@tessellum/composer-ts";

// Compile a skill → the Python compiler's DAG JSON (the plan artifact).
const dag = compile("vault/resources/skills/skill_foo.md");

// Pure control-flow over the DAG (no I/O — mirrors Python compute_ready_set):
columns(dag);                         // [["step_1"], ["step_2","step_3"], ["step_4"]]
readyFrontier(dag, new Set(["step_1"])); // ["step_2","step_3"]

// Execute — defaults to the v4 wave-parallel scheduler (run_pipeline_dynamic):
const result = run("vault/resources/skills/skill_foo.md", {
  leavesPath: "leaves.json",
  vault: "vault",
  dynamic: true,          // route through the v4 --dynamic path
  workers: 4,
  manifest: "manifest.json",   // resume manifest (Python-owned)
  closeGate: true,             // per-session close-gate
  maxInvocations: 1000,        // global budget → typed BUDGET_EXHAUSTED
  stats: "statistics.json",
});
result.error_count;       // 0 on a clean run
```

`run()` maps 1:1 onto `tessellum composer run --dynamic` flags. An exit
code of `1` (a leaf errored — e.g. a budget halt or a blocked close-gate)
is a **valid, parseable result** (`error_count > 0`), not a bridge
failure; only exit `≥ 2` (an invocation error) raises `BridgeError`.

## Tests

```bash
cd composer-ts
npm test          # 11 pure DAG-walk tests + 4 real-CLI integration tests
npm run test:unit # pure DAG tests only (no `tessellum` CLI required)
```

The integration tests spawn the real `tessellum` CLI (install the repo
with `pip install -e .` first); they skip gracefully if the CLI isn't on
`PATH`.

## Design lineage

The bridge realizes the "bridge, don't port" recommendation from the
Composer design trail (the orchestrator-scope decision and its
whole-repo broadening). The Python-side `--dynamic` path it drives is the
v4 dynamic scheduler; the pure `columns`/`readyFrontier` here mirror the
Python `compute_ready_set` functional core so both planes schedule
identically.
