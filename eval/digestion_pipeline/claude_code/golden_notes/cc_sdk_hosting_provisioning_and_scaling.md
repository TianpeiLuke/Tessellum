---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hosting
keywords:
  - provision the container
  - runtime dependencies
  - agents per host formula
  - scaling and concurrency
  - consistent hashing sessionid
  - multi-tenant isolation
  - session and state persistence
  - known limitations
  - maxturns
topics:
  - Claude Code
  - Agent SDK Hosting
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/hosting
access_control_group: ["general"]
---

# Agent SDK — Provisioning and Scaling the Host

## Overview

Once you have chosen a [session pattern](cc_sdk_session_patterns.md), self-hosting an Agent SDK agent comes down to provisioning a container, working through a fixed set of production concerns, and planning around four known limitations. This note is the operational procedure: how much RAM/disk/CPU to allocate, which dependencies the container actually needs, how to compute agents-per-host and pin sessions when scaling horizontally, and how to keep tenants isolated inside a shared container. It builds directly on [the subprocess model](cc_sdk_subprocess_model.md) (one session = one `claude` CLI subprocess), so every sizing and routing decision here follows from "each session is a long-lived process tied to local state."

## Provision the container

### Container-based sandboxing

Run the SDK inside a sandboxed container for process isolation, resource limits, network control, and an ephemeral filesystem. When choosing a provider, answer: **who runs the sandbox** (sandbox-as-a-service vs. self-hosted), **cold-start latency** (ephemeral patterns need sub-second starts; long-running tolerate more), **persistent storage** (durable volumes vs. ephemeral disk — the hybrid pattern needs durable storage somewhere), **pricing model** (per-second suits bursty ephemeral; hourly suits long-running), and **networking** (custom egress rules, outbound proxies, private VPC peering for regulated environments). The page lists Modal Sandbox, Cloudflare Sandboxes, Daytona, E2B, Fly Machines, and Vercel Sandbox as providers to evaluate. For self-hosted Docker, gVisor, and Firecracker, see [Isolation Technologies](cc_sdk_isolation_technologies.md).

### Runtime dependencies

The container needs only your SDK's language runtime: **Python 3.10+** for the Python SDK, or **Node.js 18+** for the TypeScript SDK. Both SDK packages bundle a native Claude Code binary for the host platform, so no separate Claude Code or Node.js install is needed for the spawned CLI. The bundled binary is pinned to the SDK package version, so **updating the SDK is how you update the CLI**. The SDK follows semver: take patch releases continuously and review the changelog before taking a minor.

### Resources

**1 GiB RAM, 5 GiB disk, and 1 CPU per agent** is a reasonable starting point for a freshly started instance. Memory usage grows with session length and tool activity, so size for the session lengths and concurrency you actually need rather than the idle baseline.

### Network

The SDK needs outbound HTTPS to `api.anthropic.com`, or your provider's regional endpoint on Bedrock or Vertex. If agents use [MCP servers](https://code.claude.com/docs/en/agent-sdk/mcp) or external tools, they need outbound access to those endpoints too. For production, route outbound traffic through an egress proxy that enforces domain allowlists, injects credentials, and logs requests (see [Credential and Filesystem Controls](cc_sdk_credential_and_filesystem_controls.md)). For inbound traffic, expose an HTTP or WebSocket port on the container; your application handles client requests on that port and calls the SDK internally — the subprocess itself does not listen on the network.

## Handle production concerns

- **Session and state persistence**: default local disk is lost on restart, scale-down, or a move to a different node. For any session a user expects to resume, mirror the transcript to durable storage with a [`SessionStore` adapter](https://code.claude.com/docs/en/agent-sdk/session-storage). `SessionStore` mirrors **transcripts only** (not `CLAUDE.md` or working-dir artifacts), is a **mirror, not a replacement** (local writes stay authoritative), and emits a `{ type: "system", subtype: "mirror_error" }` message without retry if the store rejects or times out — alert on these if durability matters.
- **Observability**: long-lived agents spawn tool calls across many API round-trips; without telemetry you cannot see which tools ran, how long they took, or where a session stalled. The SDK inherits OpenTelemetry config from the environment — set the OTEL variables at the container/orchestrator level (see [Observability with OpenTelemetry](cc_sdk_observability_opentelemetry.md)).
- **Auth and secrets**: the subprocess reads `ANTHROPIC_API_KEY` from its environment — supply it from your secret manager, or set `ANTHROPIC_BASE_URL` to route model calls through a key-injecting proxy. Put inbound authentication at a gateway in front of the container (the agent should receive pre-authenticated requests). Keep outbound tool credentials out of the agent environment and inject them at a proxy. See [Credential and Filesystem Controls](cc_sdk_credential_and_filesystem_controls.md).
- **Cost**: Anthropic token cost typically dominates container infrastructure cost by an order of magnitude or more — a minimally provisioned container runs roughly $0.05/hour, while a single long agent session can spend dollars in tokens. See [Cost and Usage Tracking](cc_sdk_cost_and_usage_tracking.md).

### Scaling and concurrency

Each session runs in its own subprocess, so concurrency on a host is bounded by how many subprocesses its RAM can hold. Size each host with this formula:

```text
agents per host = (host RAM - overhead) / (per-session RAM ceiling)
```

Measure the per-session ceiling by running a representative session to your target length under expected tool load and recording peak RSS; the 1 GiB starting point is a floor, not the ceiling. Horizontal-scale routing depends on your pattern. For long-running sessions, run a pool of containers behind a load balancer and **pin each session to one container using consistent hashing on `sessionId`** — a pinned session keeps hitting the same container, and therefore the same running subprocess, until it is evicted or the container restarts. Large fanouts of concurrent [subagents](https://code.claude.com/docs/en/agent-sdk/subagents) from a single session can hit API rate limits; break the work into smaller batches rather than one wide dispatch.

### Multi-tenant isolation

Default SDK behavior reads settings and `CLAUDE.md` from the filesystem, so in a shared multi-tenant container those files can leak one tenant's context into another. To isolate tenants: pass `settingSources: []` (TS) / `setting_sources=[]` (Python) so no filesystem settings load; set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env` (auto memory loads into the system prompt regardless of `settingSources`); point `CLAUDE_CONFIG_DIR` at a per-tenant directory; use a per-tenant working directory passed via `cwd` on every `query()` call; and apply per-tenant egress rules at your proxy. The four SDK-level options applied together (note: in TS `env` *replaces* the subprocess environment, so spread `...process.env` to keep `PATH`/`ANTHROPIC_API_KEY`; in Python `env` is merged):

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

declare const prompt: string;
declare const tenantDir: string;
declare const configDir: string;

for await (const message of query({
  prompt,
  options: {
    cwd: tenantDir,
    settingSources: [],
    env: {
      ...process.env,
      CLAUDE_CONFIG_DIR: configDir,
      CLAUDE_CODE_DISABLE_AUTO_MEMORY: "1",
    },
  },
})) {
  // ...
}
```

## Known limitations

Plan around these four in your deployment design:

| Limitation | What to do |
| --- | --- |
| No top-level session timeout | A session does not time out on its own. Set `maxTurns` in `Options` to bound how many tool-use round trips the agent takes before stopping. |
| Memory growth over long sessions | Cap session length or recycle subprocesses periodically. |
| Large parallel-subagent fanouts can hit rate limits | Break work into smaller batches rather than issuing one wide dispatch. |
| No per-subagent wall-clock deadline | Cap each subagent with `maxTurns` in its `AgentDefinition`. For background subagents only, `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` sets a stall watchdog that fires when a `run_in_background` subagent stops producing output; it is not a total-runtime deadline. |

**Source**: https://code.claude.com/docs/en/agent-sdk/hosting
**Last Updated**: 2026-06-13
**Status**: Active
