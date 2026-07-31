---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - message_lifecycle
keywords:
  - openclaw message lifecycle migration
  - durable send intent
  - compatibility guardrails channels
  - eight phase migration plan
  - delivery failure classes
  - unknown_after_send recovery
  - channel mapping durable delivery
  - messages.send messages.receive bridge
topics:
  - OpenClaw
  - Message Lifecycle Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/concepts/message-lifecycle-refactor
access_control_group: ["general"]
---

# OpenClaw — Message Lifecycle Refactor: Migration Plan & Compatibility

## Overview

This note argues the *migration half* of OpenClaw's message-lifecycle refactor: how to move every channel from scattered reply/dispatch helpers onto the durable `messages.receive`/`messages.send`/`messages.live`/`messages.state` domain *without breaking* existing channels. It mirrors the back half of the `concepts/message-lifecycle-refactor` source page — compatibility guardrails, durable storage (`DurableSendIntent`), delivery failure classes, the per-channel migration mapping, the eight-phase rollout, test plan, open questions, and acceptance criteria. The companion [oc_concepts_message_lifecycle_refactor_model](oc_concepts_message_lifecycle_refactor_model.md) covers the target domain model this migration phases in.

## Compatibility Guardrails

The central migration thesis is that generic durable delivery is **opt-in** for any channel whose delivery callback has side effects beyond "send this payload". Legacy entry points stay non-durable by default: `channel.inbound.run` and `dispatchChannelInboundReply` keep using the channel's delivery callback unless it supplies an audited durable policy/options object; `channel.inbound.runPreparedReply` stays channel-owned until the prepared dispatcher explicitly calls the send context; and public helpers such as `recordInboundSessionAndDispatchReply`, `dispatchInboundReplyWithBase`, and direct-DM helpers never inject generic durable delivery before the caller-provided `deliver`/`reply` callback.

For migration bridge types, `durable: undefined` means "not durable" — the durable path is enabled only by an explicit policy/options value. `durable: false` can remain as a compatibility spelling, but the implementation must not require every unmigrated channel to add it. Bridge code keeps the decision explicit via a discriminated status: `handled_visible`/`handled_no_send` are terminal; `unsupported`/`not_applicable` may fall back to channel-owned delivery; `failed` propagates the send failure. Generic durable final delivery is gated by adapter capabilities (silent delivery, reply-target/native-quote preservation, message-sending hooks); missing parity chooses channel-owned delivery, not a generic send that changes user-visible behavior. Queue-backed durable sends expose a delivery intent reference: existing `pendingFinalDelivery*` session fields carry the intent id during transition, with the end state a `MessageSendIntent` store instead of frozen reply text plus ad hoc context fields.

The generic durable path must not be enabled until **all** hold: the generic send adapter executes the same rendering/transport as the old direct path; local post-send side effects are preserved through the send context; the adapter returns receipts/delivery results with all platform message ids; prepared dispatcher paths either call the new send context or stay documented as outside the durable guarantee; fallback delivery handles every projected payload; and durable fallback records the whole projected payload array as one replayable intent or batch plan.

Concrete migration hazards the source names: iMessage durable finals must still populate the monitor echo cache (else OpenClaw re-ingests its own replies as inbound); Tlon's model signature and participated-thread tracking must move into Tlon render/send/finalize adapters or Tlon stays channel-owned; Discord and other prepared dispatchers are not covered by an assembled-turn durable guarantee until they route finals through the send context; Telegram silent fallback must deliver the full projected payload array; LINE/Zalo/Nostr paths with reply-token handling, media proxying, sent-message caches, loading/status cleanup, or callback-only targets stay channel-owned until represented by the send adapter and tested; direct-DM helpers can have a reply callback that is the only correct transport target, so generic outbound must not guess from `OriginatingTo`/`To` and skip it; and gateway-failure output stays visible while tagged bot-room echoes drop before `allowBots` via structured origin metadata, not visible-text prefix filters.

## Internal Storage

The durable queue stores message **send intents**, not reply payloads. The intent record is the unit recovered and replayed across restart:

```typescript
type DurableSendIntent = {
  id: string;
  idempotencyKey: string;
  channel: string;
  accountId?: string;
  message: ChannelMessage;
  batch?: RenderedMessageBatch;
  liveState?: LiveMessageState;
  status:
    | "pending"
    | "sending"
    | "committing"
    | "unknown_after_send"
    | "sent"
    | "failed"
    | "cancelled";
  attempt: number;
  nextAttemptAt?: number;
  receipt?: MessageReceipt;
  partialReceipt?: MessageReceipt;
  failure?: DeliveryFailure;
  createdAt: number;
  updatedAt: number;
};
```

Recovery walks pending/sending intents under an idempotency lock, then commits, marks `unknown_after_send`, or schedules a retry:

```text
load pending or sending intents
  -> acquire idempotency lock
  -> skip if receipt already committed
  -> reconstruct send context
  -> render if needed
  -> reconcile unknown_after_send if needed
  -> call adapter send/edit/finalize
  -> commit receipt, mark unknown_after_send, or schedule retry
```

The queue keeps enough identity to replay through the same account, thread, target, formatting policy, and media rules.

## Failure Classes

Channel adapters classify transport failures into a closed set for uniform retry policy:

```typescript
type DeliveryFailureKind =
  | "transient"
  | "rate_limit"
  | "auth"
  | "permission"
  | "not_found"
  | "invalid_payload"
  | "conflict"
  | "cancelled"
  | "unknown";
```

Core policy: retry `transient`/`rate_limit`; do not retry `invalid_payload` unless a render fallback exists; do not retry `auth`/`permission` until configuration changes; for `not_found`, let live finalization fall back from edit to fresh send when the channel declares that safe; for `conflict`, use receipt/idempotency rules. Any error after the adapter may have completed platform I/O but before receipt commit becomes `unknown_after_send` — unless the adapter can prove the platform operation did not happen.

## Channel Mapping

The source assigns each bundled channel a target migration shape (which adapters it needs). Highlights: **Telegram** — receive ack policy plus durable finals; live adapter owns send+edit preview, stale-preview fresh final, topics, quote-reply skip, media fallback, retry-after. **Discord** — send adapter wraps durable payload delivery; live adapter owns draft edit, progress draft, media/error preview cancel, reply-target preservation, message-id receipts. **Slack** — live adapter chooses native stream vs draft by thread shape; origin adapter maps failures to `chat.postMessage.metadata` and drops tagged bot-room echoes before `allowBots`. **WhatsApp** — durable text/media finals; live absent until an editable transport exists. **Matrix** — live adapter owns draft edits, finalization, redaction, encrypted-media constraints, reply-target mismatch fallback; origin adapter encodes failures into event content. **Mattermost / Teams / Feishu / QQ Bot** — live-centric draft/native-stream/streaming-card migrations. **Signal, iMessage, Google Chat, LINE, Nextcloud Talk, IRC, Nostr, Synology Chat, Twitch, Zalo, Zalo Personal** — simple receive+send adapters (iMessage preserves monitor echo-cache; LINE models reply-token constraints as a target/relation capability; Nostr receipts are event ids). **Tlon** — send adapter preserves model-signature rendering and participated-thread tracking first. **QA Channel** — a contract-test adapter.

## Migration Plan (Phases 1-8)

The rollout sequences eight phases so legacy behavior stays default until each surface is proven:

- **Phase 1 — Internal Message Domain.** Add `src/channels/message/*` types (messages, targets, relations, origins, receipts, capabilities, durable intents, receive/send/live contexts, failure classes); add `origin?: MessageOrigin` to the bridge payload type, then move it onto `ChannelMessage`; keep internal until adapters/tests prove the shape; add unit tests for state transitions/serialization.
- **Phase 2 — Durable Send Core.** Move the outbound queue from reply-payload durability to durable send intents (carrying a projected payload array or batch plan); preserve recovery via compatibility conversion; make `deliverOutboundPayloads` call `messages.send`; make final-send durability the default (fail closed when the intent cannot be written) only in the new lifecycle after the adapter declares replay safety — existing inbound runner/SDK paths stay direct-send; record receipts and return them to the original dispatcher caller; persist message origin through intents.
- **Phase 3 — Channel Inbound Bridge.** Reimplement `channel.inbound.run` and `dispatchChannelInboundReply` on `messages.receive`/`messages.send`; keep current fact types stable; keep legacy behavior by default (assembled-turn channel becomes durable only on explicit replay-safe opt-in); keep `durable: false` as an escape hatch without relying on `false` markers to protect unmigrated channels.
- **Phase 4 — Prepared Dispatcher Bridge.** Replace `deliverDurableInboundReplyPayload` with a send-context bridge (keep the old helper as a wrapper); port Telegram, WhatsApp, Slack, Signal, iMessage, Discord first; treat every prepared dispatcher as uncovered until it opts into the send context; keep `recordInboundSessionAndDispatchReply`, direct-DM helpers, and similar public helpers behavior-preserving.
- **Phase 5 — Unified Live Lifecycle.** Build `messages.live` with two proof adapters (Telegram send+edit+stale-final; Matrix draft finalization + redaction fallback), then migrate Discord, Slack, Mattermost, Teams, QQ Bot, Feishu; delete duplicated preview-finalization code only after each channel has parity tests.
- **Phase 6 — Public SDK.** Add `openclaw/plugin-sdk/channel-outbound` as the preferred channel plugin API; update package exports, entrypoint inventory, generated API baselines, and SDK docs; include `MessageOrigin`, origin encode/decode hooks, and the shared `shouldDropOpenClawEcho` predicate; keep compatibility wrappers; mark reply-named helpers deprecated after bundled plugins migrate.
- **Phase 7 — All Senders.** Move all non-reply outbound producers onto `messages.send`: cron/heartbeat notifications, task completions, hook results, approval prompts/results, message-tool sends, subagent announcements, explicit CLI/Control UI sends, automation/broadcast — where the model stops being "agent replies" and becomes "OpenClaw sends messages".
- **Phase 8 — Remove Turn-Named Compatibility.** Keep inbound/message-named wrappers as the compatibility window; publish migration notes; run plugin SDK compatibility tests against old imports; remove or hide old internal helpers only after no bundled plugin needs them and third-party contracts have a stable replacement.

## Test Plan

The migration's safety rests on a layered test plan. **Unit tests** cover durable send intent serialization/recovery, idempotency-key reuse and duplicate suppression, receipt commit and replay-skip, `unknown_after_send` recovery that reconciles before replay, failure-classification policy, receive-ack-policy sequencing, relation mapping (reply/followup/system/broadcast), the gateway-failure origin factory and `shouldDropOpenClawEcho` predicate, and origin preservation through normalization/chunking/serialization/recovery. **Integration tests** prove simple `channel.inbound.run` adapters still record/send, legacy assembled-event delivery stays non-durable without opt-in, the `runPreparedReply` bridge still records/finalizes, public helpers call caller-owned callbacks by default, durable fallback replays the whole projected payload array after restart, the final reply survives a restart between completion and platform send, and block/preview streaming never double-deliver text or media. **Channel tests** are per-channel parity checks (Telegram ack watermark/recovery and full projected fallback; Discord preview cancel and prepared-dispatcher routing; iMessage echo-cache; LINE/Zalo/Nostr legacy paths not bypassed; Slack tagged-echo drop ordering; Matrix finalization/redaction; Mattermost/Teams/Feishu/QQ live behaviors; Tlon signature + thread tracking; simple durable finals across the rest). **Validation** runs targeted Vitest, `pnpm check:changed`, broader `pnpm check` before landing or after public SDK/export changes, and a live/qa-channel smoke for one edit-capable and one simple send-only channel before removing wrappers.

## Open Questions

The design leaves several decisions open: whether Telegram should replace the grammY runner with a fully durable polling source controlling platform-level redelivery (not only OpenClaw's restart watermark); whether durable live-preview state belongs in the same queue record as the final send intent or a sibling store; how long compatibility wrappers stay documented after `plugin-sdk/channel-outbound` ships; whether third-party plugins implement receive adapters directly or only provide normalize/send/live hooks through `defineChannelMessageAdapter`; which receipt fields are safe to expose in the public SDK; whether side effects (self-echo caches, participated-thread markers) should be send-context hooks, adapter-owned finalize steps, or receipt subscribers; and which channels have native origin metadata versus needing persisted outbound registries or lacking reliable cross-bot echo suppression.

## Acceptance Criteria

The refactor is "done" when: every bundled channel sends final visible output through `messages.send`; every inbound channel enters through `messages.receive` or a documented wrapper; every preview/edit/stream channel uses `messages.live`; `channel.inbound` is only a wrapper; reply-named SDK helpers are compatibility exports; durable recovery replays pending finals after restart without losing the response or duplicating committed sends (unknown-outcome sends reconciled before replay or documented as at-least-once); durable finals fail closed unless a caller selected a documented non-durable mode; legacy SDK helpers default to direct channel-owned delivery with generic durable send opt-in only; receipts preserve all platform message ids plus a primary id; durable wrappers preserve channel-local side effects; prepared dispatchers are not durable until their final path uses the send context; fallback delivery handles every projected payload and records it in one replayable intent/batch plan; gateway-failure output stays visible while tagged bot-room echoes drop before bot authorization on origin-contract channels; and the docs explain send/receive/live/state, receipts, relations, failure policy, migration, and test coverage.

**Source**: OpenClaw documentation — `concepts/message-lifecycle-refactor` (mirror `inbox/openclaw_docs/concepts/message-lifecycle-refactor.md`)
**Last Updated**: 2026-06-22
**Status**: Active
