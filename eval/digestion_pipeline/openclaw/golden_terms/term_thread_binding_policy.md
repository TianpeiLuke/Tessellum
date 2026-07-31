---
tags:
  - resource
  - terminology
  - openclaw
  - channels
  - thread-binding
  - session-management
  - lifecycle-policy
  - spawn-policy
keywords:
  - Thread-Binding Policy
  - ThreadBindingSpawnPolicy
  - ThreadBindingSpawnContext
  - ThreadBindingSpawnKind
  - ThreadBindingId
  - ThreadBindingMessage
  - idle timeout
  - max age
  - spawn policy
  - chat thread session binding
  - account-scoped config
topics:
  - OpenClaw Channels
  - Thread-binding lifecycle
  - Chat-thread session management
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Thread-Binding Policy

## Definition

A **Thread-Binding Policy** is the per-channel, per-account configuration that decides whether and how an incoming chat-thread reply is allowed to bind to (or auto-spawn) an OpenClaw gateway agent session. It carries three orthogonal axes — `enabled` (is binding allowed at all), `spawnEnabled` (may a new session be auto-spawned for a `subagent` or `acp` kind), and `defaultSpawnContext` (`isolated` vs `fork` runtime) — together with two duration knobs (`idleHours`, `maxAgeHours`) that decide how long an established binding stays warm. Once the policy is resolved, the channel kernel uses it as the admission gate for every subsequent thread reply: matching threads are routed into the same session, idle threads are auto-unfocused, and over-age threads are torn down.

Conceptually it specializes the broader *session-binding* idea from web/chat platforms — Slack threads naturally cluster replies under a parent `thread_ts` so bots can scope context to one conversation [Slack threading](https://api.slack.com/messaging/threading); Discord threads expose `auto_archive_duration` so idle threads roll out of active state [Discord threads](https://discord.com/developers/docs/topics/threads). OpenClaw's thread-binding policy is the typed, account-aware equivalent of those primitives: it answers "is this thread bound to a live agent session, and if not, am I allowed to start one?" with one resolver call, then renders a human-facing intro banner so the user sees the lifecycle terms (idle window, max age) when the session opens.

## Context

The policy is implemented in `src/channels/thread-bindings-policy.ts` (257 LOC, the resolver functions and config shapes), `src/channels/thread-bindings-messages.ts` (114 LOC, the intro/farewell banner renderers), and `src/channels/thread-binding-id.ts` (17 LOC, the `${accountId}:${conversationId}` parser). It is consumed by every messaging adapter in OpenClaw — Slack-socket, Telegram, Discord-gateway, WhatsApp — at the point where the channel kernel decides between "continue an existing binding," "spawn a new session for this thread," and "ignore this message." The resolver chain is **account → channel → session → hard-coded default**, so a per-account override always wins, with the file-level constants `DEFAULT_THREAD_BINDING_IDLE_HOURS = 24` and `DEFAULT_THREAD_BINDING_MAX_AGE_HOURS = 0` (where 0 means "no cap") at the bottom.

Three industry analogs frame the position. **Session management** in general computing — a "stateful information interchange between two or more communicating devices" [Wikipedia Session](https://en.wikipedia.org/wiki/Session_(computer_science)) — provides the conceptual base; OpenClaw's thread-binding is one specialization of session lifecycle. **Slack thread continuation** — replying to a `thread_ts` keeps the conversation in the same thread; bots typically scope memory by thread root. **Discord auto-archive** — threads with `auto_archive_duration` (60 / 1440 / 4320 / 10080 minutes) automatically drop out of the active set, mirroring OpenClaw's `idleHours` knob. Where OpenClaw differs is the explicit `spawnEnabled` / `defaultSpawnContext` axes — most chat platforms don't ship a typed contract for "may this thread auto-start a new agent runtime?"

## Key Characteristics

- **Three orthogonal policy axes** — `enabled` (binding at all), `spawnEnabled` (may a new session be spawned for this thread), `defaultSpawnContext` (`fork` vs `isolated` runtime). Each axis resolves independently; even if `spawnEnabled` falls through to default, `enabled` and `defaultSpawnContext` still resolve from whichever tier first supplies a value.
- **Four-tier precedence chain** — `account-override ?? channel-override ?? session-default ?? hard-coded-default`. Per-account override is always highest precedence; the hard-coded defaults are `enabled=true`, `spawnEnabled=true`, `defaultSpawnContext="fork"`, `idleHours=24`, `maxAgeHours=0`.
- **Two duration knobs** — `idleHours` (auto-unfocus after this much inactivity) and `maxAgeHours` (hard tear-down regardless of activity; 0 = no cap). Both resolved by `resolveThreadBindingIdleTimeoutMs` and `resolveThreadBindingMaxAgeMs` via a channel-then-session-then-default fallback with `Math.floor` applied once at the end after the hours-to-ms multiplication.
- **Kind-specific spawn flags** — `spawnSubagentSessions` / `spawnAcpSessions` checked **before** the generic `spawnSessions` at each tier, so a global `spawnSessions=false` does not shadow an explicit per-kind `spawnAcpSessions=true`. The `ThreadBindingSpawnKind` discriminator (`"subagent" | "acp"`) selects which key the resolver looks up.
- **ThreadBindingId** — composite identifier of shape `${accountId}:${conversationId}`. The `resolveThreadBindingConversationIdFromBindingId` helper inverts the construction with a strict prefix-guard: a binding-id whose `accountId:` prefix does not match returns `undefined`, never a partial parse, so a binding-id from a different account cannot leak its conversation id across the account boundary.
- **ThreadBindingMessage events** — the companion `thread-bindings-messages.ts` module renders the system-prefixed intro banner (`{label} session active (idle auto-unfocus after 24h inactivity; max age 7d). Messages here go directly to this session.`) and farewell banner. The lifecycle clause is **omitted** entirely when both durations are zero — the announcement degrades to a plain "session active" line rather than printing "0" or "disabled."
- **`unknown` at every config leaf** — `SessionThreadBindingsConfigShape` types `enabled`, `idleHours`, `maxAgeHours`, `spawnSessions`, `spawnSubagentSessions`, `spawnAcpSessions`, `defaultSpawnContext` all as `unknown`. The resolver chain is the single coercion site (`normalizeBoolean`, `normalizeThreadBindingHours`, `normalizeSpawnContext`); bad config never throws at the type boundary.
- **Negative / non-finite hours coerce to `undefined`, not zero** — `normalizeThreadBindingHours` rejects bad inputs to `undefined` so the `??` chain skips them; an explicit `0` from config still beats the hard-coded default at its tier, but a `-5` does not silently masquerade as "zero hours."
- **Wire to channel kernel** — once `resolveThreadBindingSpawnPolicy` returns a flat `{ channel, accountId, enabled, spawnEnabled, defaultSpawnContext }` record, the channel kernel uses it as the gate for `runChannelTurn`'s admission ladder; `enabled=false` short-circuits to a noop dispatch.

## Related Terms


### Related Code Snippets

- **[OpenClaw Channels — Thread-Binding Policy (#672)](../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md)**: the source decomposition into the five patterns (defaults + shapes, hour resolver, spawn-policy chain, intro banner, binding-id parser).
- **[OpenClaw ACP — Spawn Thread Binding](../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md)**: the sibling ACP-side snippet that consumes the resolved policy to gate auto-spawn of an ACP session.

## References

- [Session (computer science) — Wikipedia](https://en.wikipedia.org/wiki/Session_(computer_science)) — defines a session as stateful information interchange between communicating devices with explicit lifecycle (establish / interact / terminate); thread-binding is one specialization.
- [Session management — Wikipedia](https://en.wikipedia.org/wiki/Session_management) — idle-timeout and max-age are standard session-management knobs; thread-binding policy applies the same idiom to chat threads.
- [Slack — Threading messages together](https://api.slack.com/messaging/threading) — Slack's `thread_ts` parent-reply primitive that gives chat platforms a native "thread" surface for bots to bind sessions to.
- [Discord — Threads](https://discord.com/developers/docs/topics/threads) — Discord's thread API with `auto_archive_duration` (60 / 1440 / 4320 / 10080 minutes) — the industry analog of OpenClaw's `idleHours` lifecycle knob.
- [OpenClaw — `src/channels/thread-bindings-policy.ts`](https://github.com/openclaw/openclaw/blob/main/src/channels/thread-bindings-policy.ts) — the 257-LOC implementation this term documents.
