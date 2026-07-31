---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - external_agent_bridge
keywords:
  - raft wake-channel bridge
  - RAFT_PROFILE
  - content-free wake notice
  - raft agent bridge
  - per-session shared token
  - raft message check send
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/raft
access_control_group: ["general"]
---

# Hermes Agent — Raft Setup

## Overview

Raft Setup is the messaging-integration procedure that connects Hermes to [Raft](https://raft.build) **as an external agent through a local wake-channel bridge**. It is deliberately minimal: setting a single environment variable (`RAFT_PROFILE`) auto-enables the adapter, which spawns a `raft agent bridge` child process and opens a loopback HTTP `POST /wake` endpoint. The bridge consumes wake hints from the Raft server (over SSE) and forwards each as a content-free `POST /wake`; the adapter validates a per-session shared token, verifies the payload carries no message content, and injects a short wake notice into the Hermes gateway session pipeline. The agent then reads and sends actual messages through the Raft CLI (`raft message check` / `raft message send`).

The defining design property is a strict **division of labor with a content-free wake contract**: the adapter never touches message bodies, channel names, sender identities, or delivery cursors, and holds no Raft credentials — only a per-session token used for localhost auth between the bridge and the endpoint. This keeps Hermes' messaging-gateway surface free of Raft-specific message handling and pushes all message I/O to the externally-installed Raft CLI. The gateway core it injects into (session pairing/injection, the `[SILENT]` non-reply path) is documented by the SP11a gateway notes; this note covers only the Raft adapter + bridge setup.

## Division of Labor

Source `:::info` callout, split across three owners with the adapter deliberately scoped narrow:

- **The bridge** owns: wake-hint consumption, dedup, backoff, reconnection, at-least-once delivery, and proof logging.
- **The Hermes adapter** owns: a localhost wake endpoint and injecting a short notice into the agent's context.
- **The agent** owns: pulling messages (`raft message check`), replying (`raft message send`), and all other Raft interactions via the CLI.

The adapter holds no Raft credentials — only a per-session shared token for localhost auth between the bridge and the endpoint.

## Prerequisites

- A **Raft workspace** where you can create an External Agent.
- The **Raft CLI** installed and logged in to that External Agent profile.
- **aiohttp** — Python package (included in Hermes `[all]` extras).

In Raft, open the Agents menu, create an External Agent, and follow the setup card to install the Raft CLI and log in the agent profile. Once the agent is created, Raft shows a Hermes setup guide with the environment variables and configuration needed to start the gateway.

## Setup

Add to `~/.hermes/.env`:

```bash
RAFT_PROFILE=your-agent-profile
```

That's it — the adapter auto-enables when `RAFT_PROFILE` is set. It generates a per-session bridge token, picks an ephemeral port, and spawns the bridge child process automatically when the gateway starts.

## How It Works

The data flow separates content-free wake signalling (bridge → adapter) from message-body I/O (agent → Raft server via the CLI):

```
Raft Server → Bridge (wake-hints SSE) → POST /wake → Hermes Adapter → Agent context
Agent → raft message check → Raft Server (message bodies)
Agent → raft message send → Raft Server (replies)
```

1. The Raft server sends wake hints to the bridge process via SSE.
2. The bridge forwards each hint as a `POST /wake` to the adapter's loopback endpoint.
3. The adapter validates the bridge token, verifies the payload is content-free, and injects a wake notice into the Hermes session.
4. The agent sees the wake notice and uses the Raft CLI to read messages and reply.

Wake payloads are **content-free by contract** — they carry metadata (event ID, message ID, timestamps) but never message bodies, channel names, or sender identities. The adapter rejects any payload containing content-shaped fields (`text`, `body`, `content`, `messages`, etc.).

## Bridge

The adapter automatically spawns `raft agent bridge` as a child process, passing the endpoint URL and token. The bridge connects to the Raft server using the configured profile and begins forwarding wake hints. It is terminated when the gateway shuts down.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RAFT_PROFILE` | Raft agent profile slug — auto-enables the adapter when set | _(required)_ |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/raft.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/raft
**Last Updated**: 2026-06-19
**Status**: Active
