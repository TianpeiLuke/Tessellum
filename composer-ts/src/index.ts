/**
 * composer-ts — a thin TypeScript orchestration bridge over the Python
 * Tessellum Composer substrate.
 *
 * "Bridge, don't port": TS holds control flow + DAG-walk ergonomics; the
 * Python substrate (compiler, typed contracts, materializer, gates, DB,
 * the v4 wave scheduler) stays the single source of truth, reached via
 * the `tessellum composer` CLI over a subprocess boundary. TS holds ZERO
 * contract logic, so it can never become a second, drifting authority.
 *
 * Public API:
 *   - compile(skillPath)          → the Python compiler's DAG JSON
 *   - run(skillPath, runOpts)     → the Python scheduler's RunResult
 *                                    (defaults to the v4 --dynamic path)
 *   - columns(pipeline)           → dependency-column plan (pure)
 *   - readyFrontier(pipeline,done)→ ready-set (pure; mirrors Python)
 */

export {
  compile,
  run,
  BridgeError,
} from "./bridge.ts";
export type {
  CompiledPipeline,
  CompiledStep,
  StepResult,
  RunResult,
  BridgeOptions,
  RunOptions,
} from "./bridge.ts";
export {
  runnableSteps,
  readyFrontier,
  columns,
  sideEffect,
  hasSideEffects,
} from "./dag.ts";
