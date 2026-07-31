---
tags:
  - resource
  - terminology
  - systems
  - messaging
  - agents
keywords:
  - Messaging Gateway
  - Hermes Gateway
  - chat gateway
  - platform adapter
  - hermes gateway
topics:
  - agent messaging
  - chat platform integration
  - session management
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Messaging Gateway

## Definition

A **messaging gateway** is the single background process that bridges many chat platforms to one conversational agent, isolating all platform-specific messaging code behind a uniform internal interface so the agent never has to know which surface a message came from. In the [Hermes Agent](https://github.com/NousResearch/hermes-agent), the gateway connects to 20+ configured platforms — Telegram, Discord, Slack, WhatsApp, Signal, SMS, Email, Matrix, Mattermost, Microsoft Teams, Home Assistant, an OpenAI-compatible API server, webhooks, and more — and "handles sessions, runs cron jobs, and delivers voice messages" all from one process. It is the design-pattern descendant of the enterprise-integration **Messaging Gateway** ("a class that wraps messaging-specific method calls and exposes domain-specific methods to the application"), generalized from a single message system to a fan-in over many heterogeneous chat protocols.

The gateway solves the **N-platforms-to-one-agent** problem: rather than wiring each chat service directly into agent logic, every platform is implemented as a swappable **adapter** that normalizes inbound messages into a common event, routes them through a per-chat **session store**, and dispatches them to the agent (`run_agent.py` in Hermes). Operators run it as a service (`hermes gateway` foreground, or systemd/launchd via `hermes gateway install`) so the agent is reachable remotely — "not tied to your laptop — talk to it from Telegram while it works on a cloud VM."

## Context

The messaging gateway is the chat entry point to the Hermes Agent (the other being the terminal CLI). It is operated through the `hermes gateway setup`/`start`/`stop`/`status` command set and configured per platform via `.env` keys and `~/.hermes/config.yaml` / `gateway.json`. Within the Hermes codebase it is implemented by the gateway/messaging runner module, which owns the platform-adapter registry, the per-chat session keying, the 60-second cron tick, the access-control allowlist gate, and the per-adapter circuit breaker. In this knowledge base it is the cross-cutting concept that the per-platform setup docs (Telegram, Discord, and the other team-chat surfaces) link back to rather than re-explaining the gateway. As an architectural pattern it is distinct from — and should not be confused with — an HTTP [API gateway](term_api_gateway.md), an [MCP gateway](term_mcp_gateway.md), or AWS infrastructure gateways; those route APIs/tools/network traffic, whereas a messaging gateway bridges human chat surfaces to an agent.

## Key Characteristics

- **One process, many adapters (fan-in).** Each platform is a self-contained adapter that receives messages, normalizes them, and registers into the gateway; adding a platform never touches agent logic. This is the [event-driven](term_event_driven_architecture.md) adapter fan-in: `<platform> --> session store --> AIAgent`.
- **Per-chat session store.** Inbound messages buffer through a session store keyed per chat before dispatch, so each conversation has isolated, persistent context — [sessions persist](term_session_persistence.md) across messages until a reset policy (daily / idle / both) fires.
- **Built-in cron scheduler.** A scheduler ticks every 60 seconds to execute due jobs and can deliver results to any connected platform — "daily reports, nightly backups, weekly audits … running unattended."
- **Intentional silence tokens.** If the agent's whole final response is a token (`[SILENT]`, `SILENT`, `NO_REPLY`, `NO REPLY`), the gateway suppresses outbound delivery but keeps the turn in the transcript — a delivery decision, not a state change.
- **Default-deny security.** By default the gateway denies any user not in an allowlist or paired via DM; [access control](term_access_control.md) is enforced through per-platform `*_ALLOWED_USERS` lists plus an admin/regular-user tier split that gates slash commands.
- **Resilience.** Each adapter is wrapped in a [circuit breaker](term_circuit_breaker.md) that auto-pauses on repeated retryable failures (network blips, rate-limit replies, 5xx, websocket drops) and notifies a live platform's home channel; sessions interrupted by a restart are flagged for auto-resume.
- **Capability matrix.** Platforms differ in supported features (voice, images, files, threads, reactions, typing, [streaming](term_stream_processing.md) progressive edits); the gateway exposes a per-platform toolset map so the agent's I/O degrades gracefully to each surface.
- **Deployment vs. webhook contrast.** Adapters connect via long-lived push (websocket/long-poll) or pull (polling), and some support inbound HTTP [webhooks](term_webhook.md) — but unlike a stateless webhook handler, the gateway is a persistent, stateful, multi-platform process.

## Related Terms

- **[OpenClaw — Channels & Routing Model](../documentation/openclaw/oc_channels_channel_routing.md)** — This note captures the OpenClaw **channel-routing model** — the shared target-prefix, session-key, and routing-rule grammar that every channel reuses —…

## References
- [Messaging Gateway — Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
- [NousResearch/hermes-agent — GitHub repository](https://github.com/NousResearch/hermes-agent)
- [Messaging Gateway pattern — Enterprise Integration Patterns (Hohpe & Woolf)](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessagingGateway.html)
- [Messaging pattern — Wikipedia](https://en.wikipedia.org/wiki/Messaging_pattern)
