---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - formal_verification
keywords:
  - openclaw formal verification
  - tla+ tlc security models
  - machine-checked security regression suite
  - gateway exposure model
  - node exec pipeline approvals token
  - pairing store ttl idempotency
  - ingress mention gating
  - routing session-key isolation
  - bounded model checking caveats
topics:
  - OpenClaw
  - Formal Verification
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/security/formal-verification
access_control_group: ["general"]
---

# OpenClaw — Formal Verification (Security Models)

## Overview

This note states the argument made by OpenClaw's **formal security models** (TLA+/TLC) and the explicit bounds under which that argument holds, mirroring the `security/formal-verification` source page. The page tracks an executable, attacker-driven **security regression suite**: each security claim has a runnable model-check over a finite state space, and many claims carry a paired **negative model** that produces a counterexample trace for a realistic bug class. The claim being argued is that OpenClaw enforces its intended security policy — authorization, session isolation, tool gating, and misconfiguration safety — under explicit assumptions; the argument is deliberately scoped as a regression suite, NOT a proof that "OpenClaw is secure in all respects" or that the full TypeScript implementation is correct.

## Goal, What It Is, and What It Is Not

The **goal (north star)** is to provide a machine-checked argument that OpenClaw enforces its intended security policy — authorization, session isolation, tool gating, and misconfiguration safety — under explicit assumptions. **What this is (today)** is an executable, attacker-driven security regression suite with two properties: each claim has a runnable model-check over a finite state space, and many claims have a paired negative model that produces a counterexample trace for a realistic bug class (so a regression that reintroduces the bug class re-surfaces the counterexample). **What this is not (yet)** is a proof that OpenClaw is secure in all respects, nor a proof that the full TypeScript implementation is correct — the models are abstractions checked by TLC, not the shipping code. The source also notes that some older links may refer to the previous project name.

## Where the Models Live

The models are maintained in a separate repository, [vignesh07/openclaw-formal-models](https://github.com/vignesh07/openclaw-formal-models), not in the main OpenClaw source tree. This separation matters to the argument: because the models live apart from the implementation, the suite's "green" results attest to properties of the abstract model, and any drift between that repo and the production TypeScript code is a gap the argument explicitly acknowledges (see caveats).

## Important Caveats (the Bounds of the Argument)

The strength of the formal-verification argument is bounded by three stated caveats, each of which qualifies what a "green" run is allowed to mean.

- These are **models**, not the full TypeScript implementation — drift between model and code is possible, so a green model does not certify the corresponding production code.
- Results are **bounded by the state space explored by TLC**: "green" does not imply security beyond the modeled assumptions and bounds. Beyond the explored finite states, the suite makes no claim.
- Some claims rely on **explicit environmental assumptions** (for example, correct deployment and correct configuration inputs). Where those assumptions fail, the claim does not transfer.

Together these caveats frame the suite as a regression and counterexample tool over a bounded, assumption-laden model — not an unconditional security guarantee.

## Reproducing Results (TLA+/TLC)

Today, results are reproduced by cloning the models repo locally and running TLC; the page notes that a future iteration could offer CI-run models with public artifacts (counterexample traces, run logs) and a hosted "run this model" workflow for small, bounded checks. The getting-started flow clones the repo, then invokes TLC via vendored tooling: Java 11+ is required (TLC runs on the JVM), the repo vendors a pinned `tla2tools.jar` (TLA+ tools) and provides `bin/tlc` plus Make targets, and individual checks are run as `make <target>` (the per-claim targets are enumerated below).

```bash
git clone https://github.com/vignesh07/openclaw-formal-models
cd openclaw-formal-models

# Java 11+ required (TLC runs on the JVM).
# The repo vendors a pinned `tla2tools.jar` (TLA+ tools) and provides `bin/tlc` + Make targets.

make <target>
```

## Per-Claim Models

Each model checks one security-policy claim and ships green runs (expected to pass under the model) and, where applicable, a red/negative run (expected to fail, producing a counterexample trace).

### Gateway exposure and open gateway misconfiguration

**Claim:** binding beyond loopback without auth can make remote compromise possible / increases exposure; token/password blocks unauth attackers (per the model assumptions). Green runs: `make gateway-exposure-v2` and `make gateway-exposure-v2-protected`. Red (expected): `make gateway-exposure-v2-negative`. The page also points to `docs/gateway-exposure-matrix.md` in the models repo for the exposure breakdown.

### Node exec pipeline (highest-risk capability)

**Claim:** `exec host=node` requires (a) node command allowlist plus declared commands and (b) live approval when configured; approvals are tokenized to prevent replay (in the model). Green runs: `make nodes-pipeline` and `make approvals-token`. Red (expected): `make nodes-pipeline-negative` and `make approvals-token-negative`. This is called out as the highest-risk capability, so it carries both an allowlist/approval model and a separate token-replay model.

### Pairing store (DM gating)

**Claim:** pairing requests respect TTL and pending-request caps. Green runs: `make pairing` and `make pairing-cap`. Red (expected): `make pairing-negative` and `make pairing-cap-negative`.

### Ingress gating (mentions + control-command bypass)

**Claim:** in group contexts requiring mention, an unauthorized "control command" cannot bypass mention gating. Green: `make ingress-gating`. Red (expected): `make ingress-gating-negative`.

### Routing / session-key isolation

**Claim:** DMs from distinct peers do not collapse into the same session unless explicitly linked/configured. Green: `make routing-isolation`. Red (expected): `make routing-isolation-negative`.

## v1++: Additional Bounded Models (Concurrency, Retries, Trace Correctness)

These are follow-on models that tighten fidelity around real-world failure modes — non-atomic updates, retries, and message fan-out — extending the argument from single-actor correctness toward concurrent and at-least-once-delivery realism.

### Pairing store concurrency / idempotency

**Claim:** a pairing store should enforce `MaxPending` and idempotency even under interleavings (i.e., "check-then-write" must be atomic / locked; refresh shouldn't create duplicates). What it means: under concurrent requests you cannot exceed `MaxPending` for a channel, and repeated requests/refreshes for the same `(channel, sender)` should not create duplicate live pending rows. Green runs: `make pairing-race` (atomic/locked cap check), `make pairing-idempotency`, `make pairing-refresh`, and `make pairing-refresh-race`. Red (expected): `make pairing-race-negative` (non-atomic begin/commit cap race), `make pairing-idempotency-negative`, `make pairing-refresh-negative`, and `make pairing-refresh-race-negative`.

### Ingress trace correlation / idempotency

**Claim:** ingestion should preserve trace correlation across fan-out and be idempotent under provider retries. What it means: when one external event becomes multiple internal messages, every part keeps the same trace/event identity; retries do not result in double-processing; and if provider event IDs are missing, dedupe falls back to a safe key (e.g., trace ID) to avoid dropping distinct events. Green: `make ingress-trace`, `make ingress-trace2`, `make ingress-idempotency`, and `make ingress-dedupe-fallback`. Red (expected): `make ingress-trace-negative`, `make ingress-trace2-negative`, `make ingress-idempotency-negative`, and `make ingress-dedupe-fallback-negative`.

### Routing dmScope precedence + identityLinks

**Claim:** routing must keep DM sessions isolated by default, and only collapse sessions when explicitly configured (channel precedence + identity links). What it means: channel-specific dmScope overrides must win over global defaults, and identityLinks should collapse only within explicit linked groups, not across unrelated peers. Green: `make routing-precedence` and `make routing-identitylinks`. Red (expected): `make routing-precedence-negative` and `make routing-identitylinks-negative`.

**Source**: OpenClaw documentation — `security/formal-verification` (mirror `inbox/openclaw_docs/security/formal-verification.md`)
**Last Updated**: 2026-06-22
**Status**: Active
