/**
 * bridge.ts — the TS↔Python substrate boundary.
 *
 * This is the "bridge, don't port" realization (the settled conclusion: a
 * full port is feasible-but-not-worth-it; the Python substrate stays the
 * single source of truth). The bridge shells the existing `tessellum
 * composer` CLI via child_process and parses its JSON — it holds **zero**
 * contract logic, so it can never become a second, drifting source of
 * truth. Compilation, typed-contract validation, materialization, gates,
 * and the DB all remain in Python.
 *
 * Node built-ins only — no npm dependencies. Runs under Node's native
 * TypeScript type-stripping (Node 22.6+ `--experimental-strip-types`,
 * default on 23+), so there is no build toolchain.
 */

import { spawnSync } from "node:child_process";

/** One step of a compiled pipeline, as emitted by `to_dag_json`. */
export interface CompiledStep {
  section_id: string;
  role: string; // "CORE" | "DEFERRED" | "INFRA"
  aggregation: string; // "per_leaf" | "cross_leaf" | "corpus_wide"
  batchable: boolean;
  depends_on: string[];
  materializer: {
    key: string;
    wire_format: string;
    operation_verb: string;
    required_output_fields: string[];
  } | null;
  expected_output_schema: Record<string, unknown> | null;
  output_key: string | null;
  prompt_section_text?: string;
}

/** A compiled pipeline (the Python compiler's `to_dag_json` output). */
export interface CompiledPipeline {
  format_version: string;
  skill_path: string;
  skill_name: string;
  pipeline_version: string;
  compiled_at: string;
  step_count: number;
  steps: CompiledStep[];
}

/** One (step × leaf) invocation outcome from a run. */
export interface StepResult {
  section_id: string;
  leaf_id: string | null;
  elapsed_ms: number;
  error: string | null;
  files_written: string[];
  files_applied: string[];
}

/** A run's result (the Python scheduler's JSON output). */
export interface RunResult {
  skill_name: string;
  started_at: string;
  duration_seconds: number;
  leaf_count: number;
  step_invocation_count: number;
  error_count: number;
  trace_path: string | null;
  step_results: StepResult[];
}

export interface BridgeOptions {
  /** How to invoke the CLI. Default: the `tessellum` entry point on PATH. */
  cli?: string;
  /** Extra args prepended (e.g. ["-m", "tessellum.cli.main"] for `python`). */
  cliArgs?: string[];
  /** Working directory for the subprocess. */
  cwd?: string;
  /** Max buffer for CLI stdout (bytes). Default 64 MiB. */
  maxBuffer?: number;
}

export class BridgeError extends Error {
  // Explicit fields (not constructor parameter-properties): parameter
  // properties require full TS transpilation, but Node's strip-only mode
  // only removes annotations — so we assign fields in the body instead.
  readonly code: number | null;
  readonly stderr: string;

  constructor(message: string, code: number | null, stderr: string) {
    super(message);
    this.name = "BridgeError";
    this.code = code;
    this.stderr = stderr;
  }
}

function invoke(args: string[], opts: BridgeOptions): string {
  const cli = opts.cli ?? "tessellum";
  const fullArgs = [...(opts.cliArgs ?? []), ...args];
  const res = spawnSync(cli, fullArgs, {
    cwd: opts.cwd,
    encoding: "utf-8",
    maxBuffer: opts.maxBuffer ?? 64 * 1024 * 1024,
  });
  if (res.error) {
    throw new BridgeError(
      `failed to spawn '${cli}': ${res.error.message}`,
      null,
      "",
    );
  }
  // The `run` command exits 1 when a leaf errored — that is a valid,
  // parseable result (error_count > 0), NOT a bridge failure. Only exit
  // codes >= 2 (invocation errors) or a null status are hard failures.
  if (res.status !== null && res.status >= 2) {
    throw new BridgeError(
      `'${cli} ${fullArgs.join(" ")}' exited ${res.status}`,
      res.status,
      res.stderr ?? "",
    );
  }
  return res.stdout ?? "";
}

function parseJson<T>(stdout: string, what: string): T {
  try {
    return JSON.parse(stdout) as T;
  } catch (e) {
    throw new BridgeError(
      `could not parse ${what} JSON: ${(e as Error).message}`,
      null,
      stdout.slice(0, 500),
    );
  }
}

/**
 * Compile a skill via the Python compiler and return its DAG JSON.
 * The Python side is the single validation authority — a compile error
 * surfaces as a BridgeError (exit >= 2), never a silent partial.
 */
export function compile(
  skillPath: string,
  opts: BridgeOptions = {},
  { includePrompts = true }: { includePrompts?: boolean } = {},
): CompiledPipeline {
  const args = ["composer", "compile", skillPath, "--format", "json"];
  if (!includePrompts) args.push("--no-prompts");
  const out = invoke(args, opts);
  return parseJson<CompiledPipeline>(out, "compiled pipeline");
}

export interface RunOptions {
  leavesPath?: string;
  vault?: string;
  mockResponses?: string;
  /** Route through the v4 wave-parallel scheduler (`run_pipeline_dynamic`). */
  dynamic?: boolean;
  workers?: number;
  manifest?: string;
  closeGate?: boolean;
  maxInvocations?: number;
  maxCost?: number;
  stats?: string;
  dryRun?: boolean;
  noTrace?: boolean;
}

/**
 * Execute a skill via the Python scheduler and return its RunResult.
 * By default routes through the v4 `--dynamic` path (the bridge's reason
 * to exist is to drive the wave scheduler); pass `dynamic: false` for the
 * serial reference path.
 */
export function run(
  skillPath: string,
  runOpts: RunOptions = {},
  opts: BridgeOptions = {},
): RunResult {
  const args = ["composer", "run", skillPath, "--format", "json"];
  if (runOpts.noTrace ?? true) args.push("--no-trace");
  if (runOpts.leavesPath) args.push("--leaves", runOpts.leavesPath);
  if (runOpts.vault) args.push("--vault", runOpts.vault);
  if (runOpts.mockResponses) args.push("--mock-responses", runOpts.mockResponses);
  if (runOpts.dryRun) args.push("--dry-run");
  if (runOpts.dynamic ?? true) {
    args.push("--dynamic");
    if (runOpts.workers != null) args.push("--workers", String(runOpts.workers));
    if (runOpts.manifest) args.push("--manifest", runOpts.manifest);
    if (runOpts.closeGate) args.push("--close-gate");
    if (runOpts.maxInvocations != null)
      args.push("--max-invocations", String(runOpts.maxInvocations));
    if (runOpts.maxCost != null) args.push("--max-cost", String(runOpts.maxCost));
    if (runOpts.stats) args.push("--stats", runOpts.stats);
  }
  const out = invoke(args, opts);
  return parseJson<RunResult>(out, "run result");
}
