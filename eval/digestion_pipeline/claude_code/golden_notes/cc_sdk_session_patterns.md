---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hosting
keywords:
  - session pattern
  - ephemeral session
  - long-running session
  - hybrid session
  - multi-agent container
  - container lifecycle
  - session lifetime
  - agent sdk hosting
topics:
  - Claude Code
  - Agent SDK Hosting
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/hosting
access_control_group: ["general"]
---

# Agent SDK — Choosing a Session Pattern

## Overview

When you host the Agent SDK, the first design choice is a **session pattern**: how long a container lives relative to the sessions it serves. The Agent SDK runs each agent session as a `claude` CLI subprocess that owns local state (see [SDK Subprocess Model](cc_sdk_subprocess_model.md)), so the container's lifetime, the memory it must hold, and how state survives a restart all follow from this choice. The docs name four patterns — **ephemeral**, **long-running**, **hybrid**, and **multi-agent container** — each suited to a different workload and built from a different SDK primitive. The pattern decided here pairs with a separate deployment target (local Docker, Modal, Kubernetes) from the hosting cookbook.

## The four session patterns

These four patterns cover session lifecycle: how long a container lives relative to the sessions it serves. The choice here is independent of *where* the container runs — choose a session pattern from this list and a deployment target from the cookbook.

### Ephemeral sessions

Create a container for each user task and destroy it when the task completes. Best for one-off tasks. The user may still interact with the AI while the task is completing, but once completed the container is destroyed.

Example workloads include bug investigation and fix, invoice and receipt extraction, document translation, and media transformation.

The container runs a **one-shot entrypoint** that calls the SDK and exits. The example below shows a minimal TypeScript version. Save it as `entrypoint.mts` or set `"type": "module"` in `package.json` so top-level `await` is available.

```typescript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const prompt = process.env.TASK_PROMPT!;
for await (const message of query({ prompt, options: { maxTurns: 20 } })) {
  console.log(message);
}
```

### Long-running sessions

Run persistent container instances, often hosting **multiple SDK processes per container**, to serve ongoing work. Best for agents that take autonomous action, serve content, or handle high-volume message streams.

Example workloads include an email agent that triages and responds to incoming mail, a site builder that hosts a per-user editable site through container ports, and a chat bot that handles continuous traffic from a platform like Slack.

The container exposes an HTTP or WebSocket endpoint and maps each active session to a long-lived query and the subprocess behind it. In TypeScript, use `streamInput()` to add turns to an active session and `startup()` to pre-warm subprocesses ahead of incoming traffic. In Python, use `ClaudeSDKClient` to hold a session open across turns. Size the container so it can hold the maximum number of concurrent sessions in memory.

### Hybrid sessions

Ephemeral containers that **hydrate from a `SessionStore` on startup and persist updates back**. Best for sessions that span many interactions but sit idle between them. The container spins down during idle periods and spins back up when the user returns.

Example workloads include a personal project manager with intermittent check-ins, deep research that pauses and resumes over hours, and a customer support agent that loads ticket history across interactions.

Tune your provider's idle timeout to how frequently you expect users to return. Shutting a container down without a `SessionStore` configured loses the transcript with it, so the store is **required** for this pattern, not optional.

The pattern hinges on resuming a session by ID with a shared store attached:

```typescript theme={null}
import { query, type SessionStore } from "@anthropic-ai/claude-agent-sdk";

declare const userInput: string;
declare const sessionId: string;          // looked up from your database by user
declare const sessionStore: SessionStore; // S3, Redis, Postgres, or your own adapter

for await (const message of query({
  prompt: userInput,
  options: { resume: sessionId, sessionStore },
})) {
  // ...
}
```

The Python form passes the same intent via `resume=session_id` and `session_store=session_store` on `ClaudeAgentOptions`. See [Session storage](https://code.claude.com/docs/en/agent-sdk/session-storage) for the full `SessionStore` interface and reference adapters.

### Multi-agent container

Run **multiple SDK subprocesses inside one container**. Best for agents that must collaborate closely, for example multi-agent simulations where the agents interact with each other in a shared environment.

Give each agent its own working directory so they do not overwrite each other's files, and isolate settings loading so per-agent `CLAUDE.md` files do not leak across agents. See [Multi-tenant isolation](cc_sdk_hosting_provisioning_and_scaling.md) for the specific options.

**Source**: https://code.claude.com/docs/en/agent-sdk/hosting
**Last Updated**: 2026-06-13
**Status**: Active
