---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - broadcast
keywords:
  - openclaw broadcast groups
  - whatsapp multi-agent fan-out
  - broadcast strategy parallel sequential
  - per-agent session isolation
  - broadcast config schema peerId
  - broadcast vs acp binding precedence
  - specialized agent teams
topics:
  - OpenClaw
  - Channels
  - Broadcast Groups
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/broadcast-groups
access_control_group: ["general"]
---

# OpenClaw — Broadcast Groups (WhatsApp Multi-Agent Fan-Out)

## Overview

This note is the procedure for configuring **Broadcast Groups** in OpenClaw — a feature that fans one inbound message out to multiple agents so that several specialized agents process and respond to the same message simultaneously in a single WhatsApp group or DM, all using one phone number. It mirrors the `channels/broadcast-groups` source page and covers the use cases, the top-level `broadcast` configuration block (basic setup, processing strategy, complete example), the message-flow + per-agent session-isolation model, best practices, provider/routing compatibility, troubleshooting and worked examples, the `OpenClawConfig.broadcast` config-schema reference, and the current limitations and planned enhancements. **Status: Experimental** (added in `2026.1.9`). **Current scope: WhatsApp only** (web channel). Broadcast groups are evaluated *after* channel allowlists and group activation rules, so a broadcast happens only when OpenClaw would normally reply (for example, on mention, depending on your group settings).

## Use cases

Broadcast groups let you deploy multiple agents with atomic, focused responsibilities, where each agent processes the same message and provides its specialized perspective. The source page lists four use cases: (1) **Specialized agent teams** — e.g. a "Development Team" group with `CodeReviewer` (reviews code snippets), `DocumentationBot` (generates docs), `SecurityAuditor` (checks for vulnerabilities), and `TestGenerator` (suggests test cases); (2) **Multi-language support** — an "International Support" group with `Agent_EN`, `Agent_DE`, and `Agent_ES` each responding in a different language; (3) **Quality assurance workflows** — a "Customer Support" group with a `SupportAgent` (provides the answer) and a `QAAgent` (reviews quality, only responds if issues are found); and (4) **Task automation** — a "Project Management" group with `TaskTracker` (updates task database), `TimeLogger` (logs time spent), and `ReportGenerator` (creates summaries).

## Configuration

### Basic setup

Add a top-level `broadcast` section (next to `bindings`). The keys are WhatsApp peer ids: for group chats use the group JID (e.g. `120363403215116621@g.us`); for DMs use the E.164 phone number (e.g. `+15551234567`). The value for each peer id is the array of agent IDs that should run.

```json
{
  "broadcast": {
    "120363403215116621@g.us": ["alfred", "baerbel", "assistant3"]
  }
}
```

**Result:** When OpenClaw would reply in this chat, it will run all three agents.

### Processing strategy

The optional `strategy` field controls how agents process messages. `parallel` (the default) runs all agents simultaneously. `sequential` runs the agents in array order — each one waits for the previous to finish before starting. The `strategy` key sits alongside the peer-id keys inside the `broadcast` block:

```json
{
  "broadcast": {
    "strategy": "sequential",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

### Complete example

A full configuration declares the agents under `agents.list` and then maps one or more peer ids to agent-id arrays under `broadcast`, with a single `strategy` applied across the block. Multiple peers can be configured at once — group JIDs and E.164 numbers in the same block:

```json
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

## How it works

### Message flow

A broadcast is decided through a five-step admission flow on each inbound message. (1) **Incoming message arrives** — a WhatsApp group or DM message arrives. (2) **Route and admission** — OpenClaw applies channel allowlists, group activation rules, and configured ACP binding ownership. (3) **Broadcast check** — if no configured ACP binding owns the route, OpenClaw checks whether the peer ID is in `broadcast`. (4) **If broadcast applies** — all listed agents process the message, each agent has its own session key and isolated context, and agents process in parallel (default) or sequentially. (5) **If broadcast does not apply** — OpenClaw dispatches the ordinary route or the configured ACP session route selected during routing. Broadcast groups do NOT bypass channel allowlists or group activation rules (mentions/commands/etc); they only change *which agents run* when a message is eligible for processing.

### Session isolation

Each agent in a broadcast group maintains a completely separate **session key** (e.g. `agent:alfred:whatsapp:group:120363...` vs `agent:baerbel:whatsapp:group:120363...`), **conversation history** (an agent does not see other agents' messages), **workspace** (separate sandboxes if configured), **tool access** (different allow/deny lists), and **memory/context** (separate `IDENTITY.md`, `SOUL.md`, etc.). The one shared piece is the **group context buffer** (recent group messages used for context) — it is shared per peer, so all broadcast agents see the same context when triggered. Because of this isolation, each agent can have different personalities, different tool access (e.g. read-only vs. read-write), different models (e.g. opus vs. sonnet), and different skills installed.

### Example: isolated sessions

For group `120363403215116621@g.us` with agents `["alfred", "baerbel"]`, Alfred's context resolves to session `agent:alfred:whatsapp:group:120363403215116621@g.us` with history `[user message, alfred's previous responses]`, workspace `/Users/user/openclaw-alfred/`, and tools `read, write, exec`; Bärbel's context resolves to session `agent:baerbel:whatsapp:group:120363403215116621@g.us` with history `[user message, baerbel's previous responses]`, workspace `/Users/user/openclaw-baerbel/`, and tools `read only`.

## Best practices

The source page gives five best practices. (1) **Keep agents focused** — design each agent with a single, clear responsibility (good: each agent has one job, such as `["formatter", "linter", "tester"]`; bad: one generic "dev-helper" agent). (2) **Use descriptive names** — give each agent a clear `name` (e.g. "Security Scanner", "Code Formatter", "Test Generator"). (3) **Configure different tool access** — give agents only the tools they need via `tools.allow` (e.g. a `reviewer` with `["read", "exec"]` is read-only, while a `fixer` with `["read", "write", "edit", "exec"]` can read and write). (4) **Monitor performance** — with many agents, use `"strategy": "parallel"` (default) for speed, limit broadcast groups to 5-10 agents, and use faster models for simpler agents. (5) **Handle failures gracefully** — agents fail independently and one agent's error does not block others (e.g. `Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]` results in Agent A and C responding while Agent B logs the error).

## Compatibility

### Providers

Broadcast groups currently work with: ✅ **WhatsApp** (implemented); 🚧 **Telegram** (planned); 🚧 **Discord** (planned); 🚧 **Slack** (planned).

### Routing

Broadcast groups work alongside existing routing — ordinary `bindings` and `broadcast` can coexist, with `GROUP_A` answered by only one agent through a normal route binding while `GROUP_B` is answered by all its broadcast agents:

```json
{
  "bindings": [
    {
      "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "GROUP_A" } },
      "agentId": "alfred"
    }
  ],
  "broadcast": {
    "GROUP_B": ["agent1", "agent2"]
  }
}
```

**Precedence:** `broadcast` takes priority over ordinary route bindings. Configured ACP bindings (`bindings[].type="acp"`) are exclusive: when one matches, OpenClaw dispatches to the configured ACP session instead of fan-out broadcast.

## Troubleshooting

When **agents are not responding**, check that the agent IDs exist in `agents.list`, that the peer ID format is correct (e.g. `120363403215116621@g.us`), and that the agents are not in deny lists; debug by tailing the gateway log filtered for broadcast events:

```bash
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

When **only one agent responds**, the cause is usually that the peer ID is in ordinary route bindings but not in `broadcast`, or it matches an exclusive configured ACP binding — fix it by adding ordinary route-bound peers to the broadcast config, or remove/change the configured ACP binding if fan-out broadcast is desired. For **performance issues** that appear with many agents, reduce the number of agents per group, use lighter models (sonnet instead of opus), and check sandbox startup time.

## Examples

The source page provides two worked examples. **Example 1: Code review team** uses `"strategy": "parallel"` for group `120363403215116621@g.us` with agents `["code-formatter", "security-scanner", "test-coverage", "docs-checker"]`, each declared in `agents.list` with scoped `tools.allow` (formatter `["read", "write"]`, security-scanner and test-coverage `["read", "exec"]`, docs-checker `["read"]`); when the user sends a code snippet, the responses are code-formatter ("Fixed indentation and added type hints"), security-scanner ("⚠️ SQL injection vulnerability in line 12"), test-coverage ("Coverage is 45%, missing tests for error cases"), and docs-checker ("Missing docstring for function `process_data`"). **Example 2: Multi-language support** uses `"strategy": "sequential"` for the DM peer `+15555550123` with agents `["detect-language", "translator-en", "translator-de"]`, each declared in `agents.list` with its own workspace, so the agents run in array order.

## API reference

### Config schema

The `broadcast` block is an optional top-level key on `OpenClawConfig`. It carries an optional `strategy` plus an index signature mapping each peer id to an array of agent ids:

```typescript
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

### Fields

`strategy` — type `"parallel" | "sequential"`, default `"parallel"` — how to process agents: `parallel` runs all agents simultaneously; `sequential` runs them in array order. `[peerId]` — type `string[]` — a WhatsApp group JID, E.164 number, or other peer ID; the value is the array of agent IDs that should process messages.

## Limitations

The source lists four limitations: (1) **Max agents** — no hard limit, but 10+ agents may be slow; (2) **Shared context** — agents do not see each other's responses (by design); (3) **Message ordering** — parallel responses may arrive in any order; (4) **Rate limits** — all agents count toward WhatsApp rate limits.

## Future enhancements

Planned features (not yet available): shared context mode (agents see each other's responses); agent coordination (agents can signal each other); dynamic agent selection (choose agents based on message content); and agent priorities (some agents respond before others).

**Source**: OpenClaw documentation — `channels/broadcast-groups` (mirror `inbox/openclaw_docs/channels/broadcast-groups.md`)
**Last Updated**: 2026-06-22
**Status**: Active
