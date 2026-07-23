/**
 * Pure DAG-walk tests — no subprocess, synthetic CompiledPipeline objects.
 * Run: node --test --experimental-strip-types composer-ts/test/
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import {
  runnableSteps,
  readyFrontier,
  columns,
  sideEffect,
  hasSideEffects,
} from "../src/dag.ts";
import type { CompiledPipeline, CompiledStep } from "../src/bridge.ts";

function step(
  section_id: string,
  depends_on: string[] = [],
  role = "CORE",
  verb: string | null = null,
): CompiledStep {
  return {
    section_id,
    role,
    aggregation: "per_leaf",
    batchable: false,
    depends_on,
    materializer: verb
      ? {
          key: "m",
          wire_format: "json",
          operation_verb: verb,
          required_output_fields: [],
        }
      : null,
    expected_output_schema: null,
    output_key: null,
  };
}

function pipeline(steps: CompiledStep[]): CompiledPipeline {
  return {
    format_version: "1.0",
    skill_path: "x.md",
    skill_name: "x",
    pipeline_version: "1.0",
    compiled_at: "2026-01-01T00:00:00",
    step_count: steps.length,
    steps,
  };
}

// a → {b, c} → d (diamond)
const DIAMOND = pipeline([
  step("a"),
  step("b", ["a"]),
  step("c", ["a"]),
  step("d", ["b", "c"]),
]);

test("runnableSteps drops INFRA", () => {
  const p = pipeline([step("setup", [], "INFRA"), step("work")]);
  assert.deepEqual(
    runnableSteps(p).map((s) => s.section_id),
    ["work"],
  );
});

test("readyFrontier promotes only the root first", () => {
  assert.deepEqual(readyFrontier(DIAMOND, new Set()), ["a"]);
});

test("readyFrontier promotes independent siblings together", () => {
  assert.deepEqual(readyFrontier(DIAMOND, new Set(["a"])), ["b", "c"]);
});

test("readyFrontier promotes the join once both deps are done", () => {
  assert.deepEqual(readyFrontier(DIAMOND, new Set(["a", "b", "c"])), ["d"]);
});

test("readyFrontier excludes done steps", () => {
  assert.deepEqual(readyFrontier(DIAMOND, new Set(["a", "b"])), ["c"]);
});

test("columns groups the diamond into 3 dependency columns", () => {
  assert.deepEqual(columns(DIAMOND), [["a"], ["b", "c"], ["d"]]);
});

test("columns of a linear chain is one step per column", () => {
  const chain = pipeline([step("s1"), step("s2", ["s1"]), step("s3", ["s2"])]);
  assert.deepEqual(columns(chain), [["s1"], ["s2"], ["s3"]]);
});

test("columns of fully-independent steps is a single column", () => {
  const flat = pipeline([step("a"), step("b"), step("c")]);
  assert.deepEqual(columns(flat), [["a", "b", "c"]]);
});

test("columns throws on a cycle", () => {
  // b↔c mutual dependency (the Python compiler would reject this; the TS
  // walker guards it defensively).
  const cyclic = pipeline([step("b", ["c"]), step("c", ["b"])]);
  assert.throws(() => columns(cyclic), /cycle or unknown dependency/);
});

test("sideEffect projects the materializer verb", () => {
  assert.equal(sideEffect(step("a", [], "CORE", "PRODUCE")), "PRODUCE");
  assert.equal(sideEffect(step("a", [], "CORE", "APPLY")), "APPLY");
  assert.equal(sideEffect(step("a", [], "CORE", null)), "none");
});

test("hasSideEffects is true for a producer, false for read-only", () => {
  assert.equal(hasSideEffects(pipeline([step("a", [], "CORE", "PRODUCE")])), true);
  assert.equal(hasSideEffects(pipeline([step("a", [], "CORE", "DESCRIBE")])), false);
  assert.equal(hasSideEffects(pipeline([step("a")])), false);
});
