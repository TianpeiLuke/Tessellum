---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - context_engine
keywords:
  - codex harness context engine port
  - context-engine lifecycle codex app-server
  - lossless-claw codex projection
  - assemble afterTurn maintain compact
  - codex thread/start turn/start projection
  - prompt-cache stability deterministic context
  - ownsCompaction two compaction systems
  - agentRuntime.id codex runtime selection
topics:
  - OpenClaw
  - Codex Context Engine Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/plan/codex-context-engine-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Context-Engine Port (Design Rationale + Target Contract)

## Overview

This note captures the **design rationale and target contract** half of OpenClaw's draft implementation specification `plan/codex-context-engine-harness` — the argument for why and how the bundled **Codex app-server harness** should honor the same OpenClaw **context-engine lifecycle** that embedded OpenClaw turns already honor. It mirrors the source page's `Status`, `Goal`, `Non-goals`, `Current architecture`, `Current gap`, `Desired behavior`, `Design constraints` (4 sub-constraints), `Open questions`, and `Acceptance criteria` sections. The page's front-matter declares its `read_when` triggers (wiring context-engine behavior into the Codex harness; getting `lossless-claw` or another context-engine plugin to work with `codex/*` embedded harness sessions; comparing embedded OpenClaw vs Codex app-server context behavior) and a `## Status` of **Draft implementation specification**. The sequential 10-step build runbook, test plan, observability fields, and migration notes live in the companion procedure note [oc_plan_codex_context_engine_harness_implementation](oc_plan_codex_context_engine_harness_implementation.md); this note is the durable, citable *why/what* anchor, not the *how*.

## Goal

The goal is to make the bundled Codex app-server harness honor the same OpenClaw context-engine lifecycle contract that embedded OpenClaw turns already honor. Concretely: a session using provider/model `agentRuntime.id: "codex"` or a `codex/*` model should still let the selected context-engine plugin — such as `lossless-claw` — control context assembly, post-turn ingest, maintenance, and OpenClaw-level compaction policy *as far as the Codex app-server boundary allows*. The qualifier matters: the design accepts that the Codex app-server owns an external boundary OpenClaw cannot reach into, so "as far as the boundary allows" is the operative scope, not full native-history control.

## Non-goals

The spec is deliberately narrow. It explicitly does NOT:

- Reimplement Codex app-server internals.
- Make Codex native thread compaction produce a `lossless-claw` summary.
- Require non-Codex models to use the Codex harness.
- Change ACP/acpx session behavior — this specification is for the **non-ACP embedded agent harness path only**.
- Make third-party plugins register Codex app-server extension factories; the existing **bundled-plugin trust boundary remains unchanged**.

These non-goals bound the trust and protocol surface: the work stays inside OpenClaw-controlled code and the existing bundled-plugin trust model, and treats Codex's native compactor and thread store as opaque.

## Current architecture

The argument starts from how the embedded run loop works today. The embedded run loop resolves the configured context engine **once per run** before selecting a concrete low-level harness. In `src/agents/embedded-agent-runner/run.ts` the loop initializes context-engine plugins, calls `resolveContextEngine(params.config)`, and passes `contextEngine` and `contextTokenBudget` into `runEmbeddedAttemptWithBackend(...)`. That call delegates to the selected agent harness via `src/agents/embedded-agent-runner/run/backend.ts` and `src/agents/harness/selection.ts`. The Codex app-server harness is registered by the bundled Codex plugin (`extensions/codex/index.ts`, `extensions/codex/harness.ts`), and the Codex harness implementation receives the **same `EmbeddedRunAttemptParams`** as built-in OpenClaw attempts (`extensions/codex/src/app-server/run-attempt.ts`).

The load-bearing consequence: because the Codex harness already receives the same params (including `params.contextEngine`), the required hook point is in **OpenClaw-controlled code**. The only external boundary is the Codex app-server protocol itself — OpenClaw can control what it sends to `thread/start`, `thread/resume`, and `turn/start`, and can observe notifications, but it cannot change Codex's internal thread store or native compactor.

## Current gap

The gap is that built-in OpenClaw attempts call the context-engine lifecycle directly, but Codex attempts do not. Built-in attempts perform: bootstrap/maintenance before the attempt; assemble before the model call; `afterTurn` or `ingest` after the attempt; maintenance after a successful turn; and context-engine compaction for engines that own compaction. This logic lives in `src/agents/embedded-agent-runner/run/attempt.ts`, `src/agents/embedded-agent-runner/run/attempt.context-engine-helpers.ts`, and `src/agents/embedded-agent-runner/context-engine-maintenance.ts`.

By contrast, Codex app-server attempts currently run generic agent-harness hooks and mirror the transcript, but do **not** call `params.contextEngine.bootstrap`, `params.contextEngine.assemble`, `params.contextEngine.afterTurn`, `params.contextEngine.ingestBatch`, `params.contextEngine.ingest`, or `params.contextEngine.maintain`. The relevant Codex code is `extensions/codex/src/app-server/run-attempt.ts`, `extensions/codex/src/app-server/thread-lifecycle.ts`, `extensions/codex/src/app-server/event-projector.ts`, and `extensions/codex/src/app-server/compact.ts`. This omission is the precise behavioral gap the spec closes.

## Desired behavior

For Codex harness turns, OpenClaw should preserve this lifecycle (the eleven ordered behaviors the design targets):

1. Read the mirrored OpenClaw session transcript.
2. Bootstrap the active context engine when a previous session file exists.
3. Run bootstrap maintenance when available.
4. Assemble context using the active context engine.
5. Convert the assembled context into Codex-compatible inputs.
6. Start or resume the Codex thread with developer instructions that include any context-engine `systemPromptAddition`.
7. Start the Codex turn with the assembled user-facing prompt.
8. Mirror the Codex result back into the OpenClaw transcript.
9. Call `afterTurn` if implemented, otherwise `ingestBatch`/`ingest`, using the mirrored transcript snapshot.
10. Run turn maintenance after successful non-aborted turns.
11. Preserve Codex native compaction signals and OpenClaw compaction hooks.

This is the parity target: the same conceptual sequence built-in attempts run, projected through the Codex app-server protocol rather than executed against an OpenClaw-owned model loop.

## Design constraints

Four constraints shape the design and explain why the implementation chooses *projection* over *native-history surgery*.

### Codex app-server remains canonical for native thread state

Codex owns its native thread and any internal extended history. OpenClaw should NOT try to mutate the app-server's internal history except through supported protocol calls. OpenClaw's transcript mirror remains the source for OpenClaw features: chat history; search; `/new` and `/reset` bookkeeping; future model or harness switching; and context-engine plugin state. This split (Codex = native thread truth; OpenClaw mirror = OpenClaw-feature truth) is the foundational constraint that the rest follow from.

### Context-engine assembly must be projected into Codex inputs

The context-engine interface returns OpenClaw `AgentMessage[]`, not a Codex thread patch. Codex app-server `turn/start` accepts a *current user input*, while `thread/start` and `thread/resume` accept *developer instructions*. Therefore the implementation needs a **projection layer**. The safe first version should avoid pretending it can replace Codex internal history; it should inject assembled context as deterministic prompt/developer-instruction material *around* the current turn. This is the central design decision of the spec — projection of assembled `AgentMessage[]` into the two protocol-accepted slots, not mutation of Codex's history.

### Prompt-cache stability matters

For engines like `lossless-claw`, the assembled context should be **deterministic for unchanged inputs**. The constraint forbids adding timestamps, random ids, or nondeterministic ordering to generated context text — so byte-identical inputs produce byte-identical projected context, preserving prompt-cache hits across turns.

### Runtime selection semantics do not change

Harness selection remains as-is: `runtime: "openclaw"` selects the built-in OpenClaw harness; `runtime: "codex"` selects the registered Codex harness; `runtime: "auto"` lets plugin harnesses claim supported providers; and unmatched `auto` runs use the built-in OpenClaw harness. This work changes only what happens **after** the Codex harness is selected — it does not touch which harness is chosen.

## Open questions (design decisions / recommendations)

The spec records four open questions, each with a recommended resolution that informs the contract:

1. **Should assembled context be injected entirely into the user prompt, entirely into developer instructions, or split?** Recommendation: **split** — put `systemPromptAddition` in developer instructions; put assembled transcript context in the user prompt wrapper. This best matches the current Codex protocol without mutating native thread history.
2. **Should Codex native compaction be disabled when a context engine owns compaction?** Recommendation: **no, not initially.** Codex native compaction may still be necessary to keep the app-server thread alive, but it must be reported as native Codex compaction, not as context-engine compaction.
3. **Should `before_prompt_build` run before or after context-engine assembly?** Recommendation: **after context-engine projection for Codex**, so generic harness hooks see the actual prompt/developer instructions Codex will receive. If built-in harness parity requires the opposite, encode the chosen order in tests and document it.
4. **Can Codex app-server accept a future structured context/history override?** **Unknown.** If it can, replace the text projection layer with that protocol and keep the lifecycle calls unchanged.

## Acceptance criteria

The design is satisfied when all of the following hold:

- A `codex/*` embedded harness turn invokes the selected context engine's assemble lifecycle.
- A context-engine `systemPromptAddition` affects Codex developer instructions.
- Assembled context affects the Codex turn input deterministically.
- Successful Codex turns call `afterTurn` or ingest fallback.
- Successful Codex turns run context-engine turn maintenance.
- Failed/aborted/yield-aborted turns do not run turn maintenance.
- Context-engine-owned compaction remains primary for OpenClaw/plugin state.
- Codex native compaction remains auditable as native Codex behavior.
- Existing built-in harness context-engine behavior is unchanged.
- Existing Codex harness behavior is unchanged when no non-legacy context engine is selected or when assembly fails.

These criteria double as the contract the companion implementation note's build steps, tests, and observability are measured against.

**Source**: OpenClaw documentation — `plan/codex-context-engine-harness` (mirror `inbox/openclaw_docs/plan/codex-context-engine-harness.md`), design-rationale half (Status / Goal / Non-goals / Current architecture / Current gap / Desired behavior / Design constraints / Open questions / Acceptance criteria)
**Last Updated**: 2026-06-22
**Status**: Active
