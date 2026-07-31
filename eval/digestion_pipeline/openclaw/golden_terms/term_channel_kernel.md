---
tags:
  - resource
  - terminology
  - channel-kernel
  - messaging-adapter
  - turn-dispatch
  - reply-pipeline
  - openclaw
keywords:
  - Channel Kernel
  - turn kernel
  - reply pipeline
  - at-least-once delivery
  - dispatch orchestrator
  - resolved turn
topics:
  - Messaging adapter framework
  - Event dispatch
  - OpenClaw channels architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# Channel Kernel

## Definition

A **Channel Kernel** is the substrate that every messaging-channel adapter in OpenClaw composes against to turn a raw inbound platform event (Slack message, Telegram update, Discord interaction, etc.) into a dispatched agent reply with durable, at-least-once delivery semantics. The naming echoes operating-system kernel terminology — the kernel owns scheduling (the dispatch loop), context switching (per-turn lifecycle stages), and IPC-like primitives (the reply pipeline + delivery hooks), while adapters live "in user space" supplying only the platform-specific `ingest`, `classify`, `preflight`, and `resolveTurn` functions. In OpenClaw, the kernel is implemented as `src/channels/turn/kernel.ts` (565 LOC, split into a dispatch half and a durable run-family half) and is the single contract surface that the Telegram, Slack-socket, Discord-gateway, and WhatsApp adapters all delegate to.

In the broader sense, a channel kernel is an instance of the **event-driven architecture** pattern applied to chatbot frameworks: emitters (chat platforms) push events into a dispatcher (the kernel), and consumers (the agent runtime) react asynchronously without direct coupling to the source platform [Wikipedia EDA](https://en.wikipedia.org/wiki/Event-driven_architecture). Slack Bolt's `app.event(type, fn)` and Discord.js's `Client extends AsyncEventEmitter` both expose this pattern at the framework boundary; OpenClaw's channel kernel does the same job but adds a typed admission ladder, a noop-delivery short-circuit for observe-only turns, and an `onFinalize` contract that guarantees at-least-once acknowledgment.

## Context

The Channel Kernel sits between two layers: **above** it, an adapter that implements `ChannelTurnAdapter<TRaw>` (e.g., the Slack adapter normalizes a `SlackEvent` into a `NormalizedTurnInput`); **below** it, the OpenClaw gateway agent runtime that produces reply blocks via `dispatchReplyWithBufferedBlockDispatcher`. The kernel is the only thing that talks to both. Three industry analogs frame its position:

- **Slack Bolt's `app.event` dispatcher** ([Bolt docs](https://docs.slack.dev/tools/bolt-python/concepts/event-listening/)) maps subscribed event types to listener functions with middleware chains — equivalent to OpenClaw's classify + preflight gate ladder.
- **Discord.js's `Client` event loop** ([Discord.js docs](https://discord.js.org/docs/packages/discord.js/main/Client:class)) extends `AsyncEventEmitter` and dispatches gateway opcodes to `.on(name, handler)` listeners — equivalent to OpenClaw's `runChannelTurn` ingest → emit → dispatch chain.
- **Microsoft Bot Framework / Botpress channel handlers** ([Bot Framework SDK](https://github.com/microsoft/botframework-sdk)) expose a connector layer that translates per-channel APIs into a unified Activity envelope — equivalent to OpenClaw's `AssembledChannelTurn` envelope.

The kernel is invoked once per inbound message. It emits `ChannelTurnLogEvent` structured records at every stage (`ingest`, `classify`, `preflight`, `assemble`, `record`, `dispatch`, `finalize`) so observability surfaces — logs, traces, replay tools — can reconstruct any turn end-to-end.

## Key Characteristics

- **Three public entry points** — `runPreparedChannelTurn` (fast-path for pre-assembled turns; suppresses observe-only noop dispatch), `runChannelTurn` (full ingest → finalize pipeline), and `runResolvedChannelTurn` (sugar wrapper that synthesizes an adapter from a flat `{input, resolveTurn}` shape). All three converge on the same durable-delivery substrate.
- **Inbound envelope dispatch** (`dispatchAssembledChannelTurn`, L171-L233) — public entry that resolves the reply pipeline, wires a durable-then-fallback `deliver` closure, and hands the bundle to `runPreparedChannelTurnCore` with `suppressObserveOnlyDispatch: false`.
- **Reply-pipeline factory** (`createChannelTurnReplyPipeline`, L83-L92) — a deprecated compat-shim that delegates verbatim to `createChannelReplyPipeline`, kept so legacy buffered dispatchers keep their import shape while plugins migrate to `defineChannelMessageAdapter`.
- **Admission/preflight normalization** (`isAdmission` + `normalizePreflight`, L94-L107) — type-narrowing guard plus wrapper-lift that collapses the `PreflightFacts | ChannelTurnAdmission | null` union into a uniform `PreflightFacts` so downstream code never branches on input shape.
- **No-op-friendly emit helper** (L109-L120) — stamps `channel` + `accountId` on every `ChannelTurnLogEvent` and uses `params.log?.()` so a caller without a logger gets a silent no-op rather than a NullPointerException.
- **Dispatch orchestrator with observe-only handling** — observe-only admissions still run the dispatch closure in `dispatchAssembledChannelTurn` (the visible-reply path), but in `runChannelTurn` the observe-only branch swaps in `createNoopChannelTurnDeliveryAdapter()` so the engine runs but never delivers.
- **Durable run-family with at-least-once semantics** — the try/catch around `dispatchResolvedChannelTurn` guarantees `onFinalize` runs on BOTH success and failure paths; the failure branch constructs a `failedResult`, runs finalize in an inner try/catch with an EMPTY catch (preserves the original dispatch error), emits a `finalize done` event, then re-throws.
- **Layered admission ladder** — final admission is computed as `resolved.admission ?? preflightAdmission ?? ({kind: "dispatch"} as const)`; the `as const` is load-bearing for discriminant narrowing.
- **Two-branch resolved turn** (discriminated union) — `ChannelTurnResolved` is either an `AssembledChannelTurn` (runtime owns dispatch) or a `PreparedChannelTurn` (adapter supplies `runDispatch` closure); both branches share identity fields so the kernel logs uniformly without narrowing.
- **Post-turn history cleanup** (`clearPendingHistoryAfterTurn`, L124-L134) — gated on a four-way conjunction (`isGroup && historyKey && historyMap && limit !== undefined`); uses `limit === undefined` (not `!limit`) because `limit: 0` is a meaningful "drop all" value.

## Related Terms


### Related Code Snippets

- **[OpenClaw Channels — Message Kernel Dispatch Pipeline (#665)](../code_snippets/snippet_openclaw_channels_kernel_dispatch.md)**: split 1 of 2 — inbound envelope dispatch, reply-pipeline factory, admission normalization, emit helper.
- **[OpenClaw Channels — Channel-Turn Durable Delivery (#666)](../code_snippets/snippet_openclaw_channels_kernel_durable.md)**: split 2 of 2 — the `run*ChannelTurn` family, at-least-once semantics, try/catch with onFinalize on both paths.
- **[OpenClaw Channels Adapter Contract (#664)](../code_snippets/snippet_openclaw_channels_adapter_contract.md)**: the five-method adapter interface (`ingest` / `classify` / `preflight` / `resolveTurn` / `onFinalize`) that composes against this kernel.

## Related Analysis (FZ 15)


## References

- [Event-driven architecture (Wikipedia)](https://en.wikipedia.org/wiki/Event-driven_architecture) — the architectural pattern OpenClaw's channel kernel instantiates; defines emitters, consumers, and event channels as the three core elements.
- [Slack Bolt — Listening to events](https://docs.slack.dev/tools/bolt-python/concepts/event-listening/) — Bolt's `app.event(type, fn)` listener pattern, the closest industry analog to the kernel's classify + preflight gates.
- [Discord.js — Client class](https://discord.js.org/docs/packages/discord.js/main/Client:class) — `Client extends AsyncEventEmitter`; gateway events dispatched to `.on(name, handler)` listeners, equivalent to `runChannelTurn`'s ingest-to-dispatch chain.
- [Microsoft Bot Framework SDK](https://github.com/microsoft/botframework-sdk) — connector-and-adapter architecture for multi-channel bots; the unified Activity envelope is the analog of OpenClaw's `AssembledChannelTurn`.
- [OpenClaw — `src/channels/turn/kernel.ts`](https://github.com/openclaw/openclaw/blob/main/src/channels/turn/kernel.ts) — the 565-LOC implementation this term documents.
