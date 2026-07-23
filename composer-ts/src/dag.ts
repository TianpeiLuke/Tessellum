/**
 * dag.ts — pure control-flow over a compiled pipeline's DAG.
 *
 * This is the "genuinely orchestration" layer the design said belongs in
 * TS: ready-frontier computation + column grouping over `depends_on`.
 * It is a PURE transform over the compiler's already-topologically-sorted
 * steps — no I/O, no LLM, no contract logic (the Python compiler already
 * validated the DAG and resolved dependencies; this only *walks* it).
 * Mirrors the Python `compute_ready_set` functional core so the two
 * planes agree on scheduling semantics.
 */

import type { CompiledPipeline, CompiledStep } from "./bridge.ts";

/** Runnable (non-INFRA) steps, in the compiler's topological order. */
export function runnableSteps(pipeline: CompiledPipeline): CompiledStep[] {
  return pipeline.steps.filter((s) => s.role !== "INFRA");
}

/**
 * The set of section_ids ready to run given the already-`done` set: a
 * step is ready iff every `depends_on` is done and it is not itself done.
 * Pure and deterministic (mirrors Python's `compute_ready_set`).
 */
export function readyFrontier(
  pipeline: CompiledPipeline,
  done: ReadonlySet<string>,
): string[] {
  const promoted: string[] = [];
  for (const s of runnableSteps(pipeline)) {
    if (done.has(s.section_id)) continue;
    if (s.depends_on.every((d) => done.has(d))) promoted.push(s.section_id);
  }
  return promoted;
}

/**
 * Group the runnable steps into dependency "columns" — each column is a
 * maximal set of steps whose dependencies are all satisfied by prior
 * columns. Column N can run fully in parallel; column N+1 waits on N.
 * A cycle (impossible after Python compile, but guarded) throws.
 */
export function columns(pipeline: CompiledPipeline): string[][] {
  const runnable = runnableSteps(pipeline);
  const total = runnable.length;
  const done = new Set<string>();
  const cols: string[][] = [];
  while (done.size < total) {
    const frontier = readyFrontier(pipeline, done);
    if (frontier.length === 0) {
      throw new Error(
        "dag.columns: no ready steps but work remains — cycle or unknown dependency",
      );
    }
    cols.push(frontier);
    for (const sid of frontier) done.add(sid);
  }
  return cols;
}

/** A step's side-effect verb, projected from its materializer contract. */
export function sideEffect(step: CompiledStep): "PRODUCE" | "APPLY" | "DESCRIBE" | "none" {
  const verb = step.materializer?.operation_verb;
  if (verb === "PRODUCE" || verb === "APPLY" || verb === "DESCRIBE") return verb;
  return "none";
}

/** True iff the pipeline writes/edits any vault file (has a PRODUCE/APPLY step). */
export function hasSideEffects(pipeline: CompiledPipeline): boolean {
  return runnableSteps(pipeline).some((s) => {
    const e = sideEffect(s);
    return e === "PRODUCE" || e === "APPLY";
  });
}
