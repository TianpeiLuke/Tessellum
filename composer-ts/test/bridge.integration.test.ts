/**
 * Integration tests — spawn the REAL `tessellum composer` CLI and prove
 * the TS↔Python boundary works end-to-end (compile + v4 --dynamic run).
 *
 * Requires the `tessellum` CLI on PATH (pip install -e . in the repo).
 * Run: node --test --experimental-strip-types composer-ts/test/
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, rmSync, existsSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

import { compile, run } from "../src/index.ts";
import { columns } from "../src/dag.ts";

const CLI = "tessellum";

// Skip the whole suite gracefully if the CLI isn't installed (keeps the
// pure dag.test.ts runnable anywhere).
const cliAvailable = (() => {
  const r = spawnSync(CLI, ["--help"], { encoding: "utf-8" });
  return r.status === 0 || (r.status !== null && r.status < 2);
})();

const SKILL_MD = `---
tags:
  - resource
  - skill
keywords:
  - alpha
  - beta
  - gamma
topics:
  - X
language: markdown
date of note: 2026-05-10
status: active
building_block: procedure
pipeline_metadata: ./skill_bridge_demo.pipeline.yaml
---

# skill_bridge_demo

## Step 1: rate <!-- :: section_id = step_1 :: -->

Rate leaf {{leaf.id}}.

## Step 2: summarize <!-- :: section_id = step_2 :: -->

Summarize {{upstream.rating}}.
`;

const SKILL_YAML = `version: "1.0"
pipeline:
  - section_id: step_1
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    prompt_template: "Rate."
    output_key: rating
  - section_id: step_2
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: [step_1]
    materializer: no_op
    prompt_template: "Summarize."
`;

function scratch(): { dir: string; skill: string; leaves: string; cleanup: () => void } {
  const dir = mkdtempSync(join(tmpdir(), "composer-ts-"));
  const skill = join(dir, "skill_bridge_demo.md");
  writeFileSync(skill, SKILL_MD);
  writeFileSync(join(dir, "skill_bridge_demo.pipeline.yaml"), SKILL_YAML);
  const leaves = join(dir, "leaves.json");
  writeFileSync(leaves, JSON.stringify([{ id: "a" }, { id: "b" }, { id: "c" }]));
  return { dir, skill, leaves, cleanup: () => rmSync(dir, { recursive: true, force: true }) };
}

test("compile() returns the Python compiler's DAG JSON", { skip: !cliAvailable }, () => {
  const s = scratch();
  try {
    const p = compile(s.skill, { cli: CLI });
    assert.equal(p.skill_name, "skill_bridge_demo");
    assert.equal(p.step_count, 2);
    assert.equal(p.steps[0].section_id, "step_1");
    assert.deepEqual(p.steps[1].depends_on, ["step_1"]);
    // The pure TS walker agrees with the Python-compiled DAG: step_1 then step_2.
    assert.deepEqual(columns(p), [["step_1"], ["step_2"]]);
  } finally {
    s.cleanup();
  }
});

test("run() drives the v4 --dynamic scheduler end-to-end", { skip: !cliAvailable }, () => {
  const s = scratch();
  try {
    const res = run(
      s.skill,
      { leavesPath: s.leaves, vault: join(s.dir, "vault"), dynamic: true, workers: 3 },
      { cli: CLI },
    );
    assert.equal(res.skill_name, "skill_bridge_demo");
    assert.equal(res.error_count, 0);
    // 3 leaves × step_1 (per_leaf) + 1 corpus × step_2 = 4 invocations.
    assert.equal(res.step_invocation_count, 4);
  } finally {
    s.cleanup();
  }
});

test("run() activates the manifest + stats sidecars via the bridge", { skip: !cliAvailable }, () => {
  const s = scratch();
  try {
    const manifest = join(s.dir, "manifest.json");
    const stats = join(s.dir, "statistics.json");
    const res = run(
      s.skill,
      {
        leavesPath: s.leaves,
        vault: join(s.dir, "vault"),
        dynamic: true,
        manifest,
        stats,
      },
      { cli: CLI },
    );
    assert.equal(res.error_count, 0);
    assert.ok(existsSync(manifest), "manifest written by the Python substrate");
    assert.ok(existsSync(stats), "statistics.json written");
    const m = JSON.parse(readFileSync(manifest, "utf-8"));
    const statuses = new Set(Object.values(m.entries).map((e: any) => e.status));
    assert.deepEqual([...statuses], ["done"]);
    const st = JSON.parse(readFileSync(stats, "utf-8"));
    assert.equal(st.invocation_count, 4);
  } finally {
    s.cleanup();
  }
});

test("run() budget halt surfaces as a parseable non-crash result", { skip: !cliAvailable }, () => {
  const s = scratch();
  try {
    // Budget below the leaf count → some leaves halt with BUDGET_EXHAUSTED.
    // The CLI exits 1 (leaf errors); the bridge must still parse the result
    // (exit 1 is a valid result, not a bridge failure — only exit >= 2 is).
    const res = run(
      s.skill,
      {
        leavesPath: s.leaves,
        vault: join(s.dir, "vault"),
        dynamic: true,
        workers: 1,
        maxInvocations: 2,
      },
      { cli: CLI },
    );
    assert.ok(res.error_count >= 1, "budget-halted leaves surface as errors");
    const budgetErrs = res.step_results.filter(
      (r) => r.error && r.error.includes("budget exhausted"),
    );
    assert.ok(budgetErrs.length >= 1);
  } finally {
    s.cleanup();
  }
});
