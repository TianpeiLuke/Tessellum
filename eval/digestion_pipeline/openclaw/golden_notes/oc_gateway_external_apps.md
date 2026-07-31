---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - external_apps
keywords:
  - openclaw external apps integration
  - gateway websocket rpc
  - agent agent.wait rpc
  - sessions rpc durable state
  - app code vs plugin code
  - no public npm client yet
  - openclaw agent cli integration
  - pin openclaw version
topics:
  - OpenClaw
  - Gateway Integration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/external-apps
access_control_group: ["general"]
---

# OpenClaw — Gateway Integrations for External Apps

## Overview

This note is the procedure for integrating code that runs **outside the OpenClaw process** — external apps, scripts, dashboards, CI jobs, and IDE extensions — with OpenClaw, mirroring the `gateway/external-apps` source page. The single supported path today is the **Gateway protocol**: connect over Gateway WebSocket and call documented RPC methods to start agent runs, stream events, wait for results, cancel work, or inspect Gateway resources. The note enumerates the surfaces available today, walks the recommended connect-and-pin sequence, and draws the app-code-vs-plugin-code boundary (when to use Gateway RPC versus the Plugin SDK). Two constraints are load-bearing: there is **no public npm client package yet**, and external apps must **not** import `openclaw/plugin-sdk/*` subpaths (those are for plugins loaded inside OpenClaw).

## Who this is for

Per the source `read_when`, follow this procedure when you are building an external app, script, dashboard, CI job, or IDE extension that talks to OpenClaw; when you are choosing between Gateway RPC and the Plugin SDK; or when you are integrating with Gateway agent runs, sessions, events, approvals, models, or tools. External apps should talk to OpenClaw through the Gateway protocol today — use Gateway WebSocket and RPC methods when a script, dashboard, CI job, IDE extension, or another process wants to start agent runs, stream events, wait for results, cancel work, or inspect Gateway resources.

## What is available today

The source page lists four ready integration surfaces. All four are marked **Ready**:

| Surface | Status | Use it for |
| --- | --- | --- |
| Gateway protocol (`/gateway/protocol`) | Ready | WebSocket transport, connect handshake, auth scopes, protocol versioning, and events. |
| Gateway RPC reference (`/reference/rpc`) | Ready | Current Gateway methods for agents, sessions, tasks, models, tools, artifacts, and approvals. |
| `openclaw agent` (`/cli/agent`) | Ready | One-shot script integration when shelling out to the CLI is enough. |
| `openclaw message` (`/cli/message`) | Ready | Sending messages or channel actions from scripts. |

The source tree contains **internal package work for a future client library**, but that is not a public install surface — treat it as preview implementation detail until the packages are published and versioned. A `<Warning>` on the page is explicit: **there is no public npm client package yet**, and you must not add OpenClaw client package names as application dependencies until release notes announce a published package and this page includes install instructions.

## Recommended path

The page prescribes a five-step connect-and-pin procedure for an external integration:

1. Run or discover a Gateway.
2. Connect over the **Gateway protocol** (`/gateway/protocol`).
3. Call documented RPC methods from the **Gateway RPC reference** (`/reference/rpc`).
4. **Pin** the OpenClaw version you test against.
5. **Recheck** the RPC reference when upgrading OpenClaw.

Within that path, the page gives three method-selection rules. For **agent runs**, start with the `agent` RPC and pair it with `agent.wait` when you need a terminal result. For **durable conversation state**, use the `sessions.*` methods. For **UI integrations**, subscribe to Gateway events and render only the event families your app understands.

## App code vs plugin code

The decisive boundary is *where the code runs*. Use **Gateway RPC** when code lives outside OpenClaw:

- Node scripts that start or observe agent runs
- CI jobs that call a Gateway
- dashboards and admin panels
- IDE extensions
- external bridges that do not need to become channel plugins
- integration tests with fake or real Gateway transports

Use the **Plugin SDK** when code runs inside OpenClaw:

- provider plugins
- channel plugins
- tool or lifecycle hooks
- agent harness plugins
- trusted runtime helpers

The page closes this section with a hard rule: external apps should **not** import `openclaw/plugin-sdk/*`; those subpaths are for plugins loaded by OpenClaw. The `<Note>` at the top of the page restates the same boundary — this page is for code outside the OpenClaw process, and plugin code that runs inside OpenClaw should use documented `openclaw/plugin-sdk/*` subpaths instead.

**Source**: OpenClaw documentation — `gateway/external-apps` (mirror `inbox/openclaw_docs/gateway/external-apps.md`)
**Last Updated**: 2026-06-22
**Status**: Active
