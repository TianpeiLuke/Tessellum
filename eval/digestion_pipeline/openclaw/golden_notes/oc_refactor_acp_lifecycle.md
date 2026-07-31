---
tags:
  - resource
  - documentation
  - openclaw
  - refactor
  - acp
keywords:
  - openclaw acp lifecycle refactor
  - acp session ownership rows
  - acpx process leases
  - gateway instance identity
  - acpx lifecycle controller
  - session visibility contract tree all
  - lease-first cleanup fail-closed
  - cancel versus close acp session
topics:
  - OpenClaw
  - ACP Lifecycle Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/refactor/acp
access_control_group: ["general"]
---

# OpenClaw — ACP Lifecycle Refactor (Explicit Session + Process Ownership)

## Overview

This note captures the OpenClaw `refactor/acp` design argument: the plan to make ACP session and ACPX process ownership **first-class** instead of inferred after the fact. Today, process cleanup reconstructs ownership from PIDs, command strings, wrapper paths, and the live process table, while session visibility reconstructs ownership from session-key strings plus secondary `sessions.list({ spawnedBy })` lookups — which makes narrow fixes possible but lets edge cases slip (PID reuse, quoted commands, adapter grandchildren, multi-gateway state roots, `cancel` versus `close`, and `tree` versus `all` visibility each become a separate place to rediscover the same ownership rules). The argument is that a safer internal contract — gateway-instance identity, normalized session-ownership rows, and ACPX process leases — replaces those heuristics. It mirrors the `refactor/acp` source page in full: Goals, Non-goals, the Target Model (gateway instance identity, ACP session ownership, ACPX process leases), the lifecycle controller, wrapper contract, session-visibility contract, the five-phase migration plan, the test suites, compatibility notes, and success criteria. The stated thesis is that the goal is **not** a new ACP product surface but a safer internal contract for existing ACP and ACPX behavior.

## Goals and Non-goals

The refactor's goals define what "ownership is first-class" must achieve. Cleanup never signals a process unless current live evidence matches an OpenClaw-owned lease. `cancel`, `close`, and startup reaping have distinct lifecycle intents. `sessions_list`, `sessions_history`, `sessions_send`, and status checks all use the same requester-owned session model. Multi-gateway installs cannot reap each other's ACPX wrappers. Old ACPX session records keep working during migration. The runtime remains plugin-owned; core does not learn ACPX package details.

The non-goals bound the change so it stays an internal-contract refactor. It does not replace ACPX or change the public `/acp` command surface, does not move vendor-specific ACP adapter behavior into core, does not require users to manually clean state before upgrading, and does not make `cancel` close reusable ACP sessions.

## Target Model

The target model introduces three durable ownership facts so that both process cleanup and session visibility become pure checks over recorded metadata rather than after-the-fact reconstruction.

### Gateway Instance Identity

Each Gateway process should have a stable runtime instance id, generated on Gateway startup and persisted in state for the life of that install. It is **not** a security secret; it is an ownership discriminator used to avoid confusing one Gateway's ACP processes with another Gateway's processes (the basis for the "multi-gateway installs cannot reap each other's wrappers" goal). The type is:

```ts
type GatewayInstanceId = string;
```

### ACP Session Ownership

Every spawned ACP session should carry normalized ownership metadata, and the Gateway should return these fields on session rows where they are known:

```ts
type AcpSessionOwner = {
  sessionKey: string;
  spawnedBy?: string;
  parentSessionKey?: string;
  ownerSessionKey: string;
  agentId: string;
  backend: "acpx";
  gatewayInstanceId: GatewayInstanceId;
  createdAt: number;
};
```

With these rows present, visibility filtering becomes a pure check over row metadata via `canSeeSessionRow({ row, requesterSessionKey, visibility, a2aPolicy })`. That removes hidden secondary `sessions.list({ spawnedBy })` calls from visibility checks: a spawned cross-agent ACP child is requester-owned because the row says so, not because a second query happens to find it.

### ACPX Process Leases

Every generated wrapper launch should create a lease record so cleanup can verify ownership against recorded facts rather than guessing from the live process table:

```ts
type AcpxProcessLease = {
  leaseId: string;
  gatewayInstanceId: GatewayInstanceId;
  sessionKey: string;
  wrapperRoot: string;
  wrapperPath: string;
  rootPid: number;
  processGroupId?: number;
  commandHash: string;
  startedAt: number;
  state: "open" | "closing" | "closed" | "lost";
};
```

The wrapper process should receive the lease id and gateway instance id in its environment as `OPENCLAW_ACPX_LEASE_ID=...` and `OPENCLAW_GATEWAY_INSTANCE_ID=...`. When the platform allows it, verification should prefer live process metadata that cannot be confused by command quoting: the root PID still exists, the live wrapper path is under `wrapperRoot`, the process group matches the lease when available, the environment contains the expected lease id when readable, and the command hash or executable path matches the lease. The fail-closed rule is explicit: **if the live process cannot be verified, cleanup fails closed** (does not signal).

## Lifecycle Controller

The argument centralizes policy into one ACPX lifecycle controller that owns process leases and cleanup policy, replacing the scattered ownership-inference sites:

```ts
interface AcpxLifecycleController {
  ensureSession(input: AcpRuntimeEnsureInput): Promise<AcpRuntimeHandle>;
  cancelTurn(handle: AcpRuntimeHandle): Promise<void>;
  closeSession(input: {
    handle: AcpRuntimeHandle;
    discardPersistentState?: boolean;
    reason?: string;
  }): Promise<void>;
  reapStartupOrphans(): Promise<void>;
  verifyOwnedTree(lease: AcpxProcessLease): Promise<OwnedProcessTree | null>;
}
```

The three lifecycle intents stay distinct. `cancelTurn` requests turn cancellation only; it must **not** reap reusable wrapper or adapter processes. `closeSession` is allowed to reap, but only after loading the session record, loading the lease, and verifying the live process tree still belongs to that lease. `reapStartupOrphans` starts from open leases in state; it may use the process table to find descendants, but it should not scan arbitrary ACP-looking commands first and then decide they are probably ours.

## Wrapper Contract

Generated wrappers should stay small and only enforce local process-tree cleanup for their own adapter group — they should **not** decide session policy. A wrapper should: start the adapter in a process group where supported; forward normal termination signals to the process group; detect parent death; on parent death, send SIGTERM, then keep the wrapper alive until the SIGKILL fallback runs; and report root PID and process group id back to the lifecycle controller when that is available.

## Session Visibility Contract

Visibility uses normalized row ownership rather than re-derived session-key strings, taking a typed input:

```ts
type SessionVisibilityInput = {
  requesterSessionKey: string;
  row: {
    key: string;
    agentId: string;
    ownerSessionKey?: string;
    spawnedBy?: string;
    parentSessionKey?: string;
  };
  visibility: "self" | "tree" | "agent" | "all";
  a2aPolicy: AgentToAgentPolicy;
};
```

The four visibility rules are: `self` returns only the requester session; `tree` returns the requester session plus rows owned by or spawned from the requester; `all` returns all same-agent rows, a2a-allowed cross-agent rows, and requester-owned spawned cross-agent rows even when general a2a is disabled; `agent` returns the same agent only, unless an explicit owner relationship says the row belongs to the requester. The load-bearing invariant of the design is that `tree` and `all` are **monotonic**: `all` must not hide an owned child that `tree` would show.

## Migration Plan

The cut-over is staged across five phases so old ACPX session records keep working during migration and legacy heuristics are removed only after a release window.

**Phase 1 — Add Identity And Leases.** Add `gatewayInstanceId` to Gateway state; add an ACPX lease store under the ACPX state directory; write a lease before spawning a generated wrapper; store `leaseId` on new ACPX session records; keep existing PID and command fields for old records.

**Phase 2 — Lease-First Cleanup.** Change close cleanup to load `leaseId` first; verify live process ownership against the lease before signaling; keep the current root PID and wrapper-root fallback only for legacy records; mark leases `closed` after verified cleanup; mark leases `lost` when the process is gone before cleanup.

**Phase 3 — Lease-First Startup Reaping.** Startup reaping scans open leases; for each lease, verify the root process and collect descendants; reap verified trees children-first; expire old `closed` and `lost` leases with a bounded retention window; keep command-marker scanning only as a temporary legacy fallback, guarded by wrapper root and Gateway instance where possible.

**Phase 4 — Session Ownership Rows.** Add ownership metadata to Gateway session rows; teach ACPX, subagent, background-task, and session-store writers to populate `ownerSessionKey` or `spawnedBy`; convert session visibility checks to use row metadata; remove visibility-time secondary `sessions.list({ spawnedBy })` lookups.

**Phase 5 — Remove Legacy Heuristics.** After one release window: stop relying on stored root command strings for non-legacy ACPX cleanup; remove command-marker startup scans; remove visibility fallback list lookups; keep defensive fail-closed behavior for missing or unverifiable leases.

## Tests

The plan adds two table-driven suites to lock the invariants. The **process lifecycle simulator** covers: a PID reused by an unrelated process; a PID reused by another Gateway's wrapper root; a stored wrapper command that is shell-quoted while the live `ps` command is not; an adapter child exiting while a grandchild remains in the process group; the parent-death SIGTERM fallback reaching SIGKILL; process listing unavailable; a stale lease with a missing process; and a startup orphan with wrapper, adapter child, and grandchild. The **session visibility matrix** covers: `self`, `tree`, `agent`, `all`; a2a enabled and disabled; same-agent row; cross-agent row; a requester-owned spawned cross-agent ACP row; a sandboxed requester clamped to `tree`; and the list, history, send, and status actions. The important invariant the tests enforce: a requester-owned spawned child is visible wherever the configured visibility includes the requester session tree, and `all` is not less capable than `tree`.

## Compatibility Notes

Old session records may not have `leaseId`, so they use the legacy fail-closed cleanup path: require a live root process; require wrapper-root ownership when a generated wrapper is expected; require command agreement for non-wrapper roots; and never signal based only on stale stored PID metadata. If a legacy record cannot be verified, **leave it alone** — startup lease cleanup and the next release window should eventually retire the fallback.

## Success Criteria

The refactor is done when: closing an old or stale ACPX session cannot kill another Gateway's process; parent death does not leave stubborn adapter grandchildren running; `cancel` aborts the active turn without closing reusable sessions; `sessions_list` can show requester-owned cross-agent ACP children under both `tree` and `all`; startup cleanup is driven by leases, not broad command-string scans; and the focused process and visibility matrix tests cover every edge case that previously required one-off review fixes.

**Source**: OpenClaw documentation — `refactor/acp` (mirror `inbox/openclaw_docs/refactor/acp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
