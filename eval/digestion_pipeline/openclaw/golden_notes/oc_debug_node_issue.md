---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - debug
keywords:
  - openclaw __name is not a function
  - node tsx crash openclaw
  - esbuild keepnames __name helper
  - createsubsystemlogger typeerror
  - auth-profiles constants tsx
  - bun to tsx regression 2871657e
  - node 25 tsx loader crash
  - tsgo node openclaw.mjs workaround
topics:
  - OpenClaw
  - Node + tsx Debugging
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/debug/node-issue
access_control_group: ["general"]
---

# OpenClaw — Node + tsx `__name is not a function` Startup Crash

## Overview

This note argues a single diagnosis: running OpenClaw from source under Node with the `tsx` loader fails at startup with `TypeError: __name is not a function`, and the load-bearing claim is that esbuild's `keepNames` `__name` helper is missing or overwritten in the Node 25 loader path. It mirrors the `debug/node-issue` source page end-to-end — the failing `createSubsystemLogger` / `auth-profiles/constants.ts` stack trace, the affected environment (Node 25.x, `tsx` 4.21.0, macOS), the Node-only repro plus the in-repo minimal repro, the Node-version test matrix, the root-cause hypothesis, the Bun→tsx regression (commit `2871657e`, 2026-01-06), the workarounds (use Bun, build then run `node openclaw.mjs`, type-check with `tsgo`), and the next steps. The root cause is presented as a hypothesis (the source flags it as such), so this note keeps that uncertainty explicit rather than asserting a confirmed fix.

## Symptom and Failing Stack Trace

Running OpenClaw via Node with `tsx` fails at startup with the following error and stack — the CLI never finishes booting:

```
[openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

The two frames are load-bearing for the diagnosis: the crash originates in `createSubsystemLogger` at `src/logging/subsystem.ts:203:25` and is reached from `src/agents/auth-profiles/constants.ts:25:20`. Both are early harness-startup modules (subsystem logging and auth-profile constants), not user code — which is why the failure surfaces as `Failed to start CLI` before any command runs. The same runtime path worked previously under Bun; the breakage began after switching dev scripts from Bun to `tsx`.

## Affected Environment

The crash is observed in this environment:

- Node: v25.x (observed on v25.3.0)
- tsx: 4.21.0
- OS: macOS (repro also likely on other platforms that run Node 25)

The macOS observation is not believed to be platform-specific — the source notes the repro is "also likely on other platforms that run Node 25", framing the failure as a Node-runtime/loader problem rather than an OS problem.

## Reproduction

Two reproduction paths are given. The full Node-only repro (run from the repo root) installs dependencies and launches `openclaw status` through the Node `tsx` import loader:

```bash
# in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

A minimal in-repo repro isolates the same loader crash without the full CLI entry, using a dedicated repro script:

```bash
node --import tsx scripts/repro/tsx-name-repro.ts
```

The repro command `node --import tsx ...` is the operative trigger: it is the on-the-fly TS→ESM transform via the `tsx`/esbuild loader, which is exactly the path that injects (or fails to inject) the `__name` helper.

## Node Version Test Matrix

The version-dependence is the core of the diagnosis, and the page records a partial matrix:

- Node 25.3.0: fails
- Node 22.22.0 (Homebrew `node@22`): fails
- Node 24: not installed here yet; needs verification

Note that both Node 25.3.0 and Node 22.22.0 (an LTS line) reproduce the failure, so the "Node 25–specific" framing is not yet confirmed — Node 24 remains untested. This open data point is why "Repro on Node 22/24 to confirm Node 25 regression" appears under Next steps.

## Root-Cause Hypothesis (esbuild `keepNames` / `__name`)

The proposed root cause is explicitly a hypothesis, not a confirmed conclusion:

- `tsx` uses esbuild to transform TS/ESM. esbuild's `keepNames` emits a `__name` helper and wraps function definitions with `__name(...)`.
- The crash indicates `__name` exists but is not a function at runtime, which implies the helper is missing or overwritten for this module in the Node 25 loader path.
- Similar `__name` helper issues have been reported in other esbuild consumers when the helper is missing or rewritten.

In other words, the argument is: esbuild's `keepNames` option injects a `__name` runtime helper to preserve original function names through minification/transform; under the Node loader path in this environment the helper is present in name but not callable (`exists but is not a function`), so the wrapped function definitions throw at startup. The cross-consumer reports (referenced below) are cited as supporting circumstantial evidence, not proof.

## Regression History (Bun → tsx)

The failure is tied to a specific dev-script change:

- `2871657e` (2026-01-06): scripts changed from Bun to tsx to make Bun optional.
- Before that (Bun path), `openclaw status` and `gateway:watch` worked.

This commit (`2871657e`) is the regression boundary: making Bun optional moved the default dev/watch path onto the Node + `tsx` loader, exposing the `__name` helper problem that the Bun runtime did not hit. The previously-working commands (`openclaw status`, `gateway:watch`) are the same ones that now fail, which is what frames this as a regression rather than a never-worked configuration.

## Workarounds

The page lists several mitigations, ordered roughly from "in use now" to "speculative":

- Use Bun for dev scripts (current temporary revert).
- Use `tsgo` for repo type checking, then run the built output:

  ```bash
  pnpm tsgo
  node openclaw.mjs status
  ```

- Historical note: `tsc` was used here while debugging this Node/tsx issue, but repo type-check lanes now use `tsgo`.
- Disable esbuild keepNames in the TS loader if possible (prevents `__name` helper insertion); tsx does not currently expose this.
- Test Node LTS (22/24) with `tsx` to see if the issue is Node 25–specific.

The strongest practical workarounds are the first two: reverting dev scripts to Bun sidesteps the `tsx` loader entirely, and the `tsgo` + `node openclaw.mjs status` path type-checks then runs the *built* output (a prebuilt `.mjs`) instead of transforming TS on the fly — avoiding the loader-injected `__name` helper. The "disable keepNames" mitigation is flagged as not currently actionable because `tsx` does not expose that esbuild option.

## Next Steps

Open follow-ups recorded on the page:

- Repro on Node 22/24 to confirm Node 25 regression.
- Test `tsx` nightly or pin to earlier version if a known regression exists.
- If reproduces on Node LTS, file a minimal repro upstream with the `__name` stack trace.

These steps target the unresolved part of the diagnosis: confirming the Node-version boundary (since Node 22.22.0 already fails, the "Node 25 regression" label needs the Node 24 data point and a clean comparison), checking whether a `tsx`/esbuild version change is the real culprit (pin/nightly), and escalating upstream with the minimal repro if the failure survives on an LTS Node.

**Source**: OpenClaw documentation — `debug/node-issue` (mirror `inbox/openclaw_docs/debug/node-issue.md`)
**Last Updated**: 2026-06-22
**Status**: Active
