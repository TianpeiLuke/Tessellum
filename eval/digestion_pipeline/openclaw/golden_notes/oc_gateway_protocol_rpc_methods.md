---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway rpc methods
  - hello-ok features methods
  - task ledger rpcs tasks.list
  - tools.catalog tools.effective tools.invoke
  - models.list views configured all
  - exec.approval.request exec.approval.resolve
  - common event families chat session
  - agent delivery fallback bestEffortDeliver
topics:
  - OpenClaw
  - Gateway Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/protocol
access_control_group: ["general"]
---

# OpenClaw — Gateway Protocol RPC Method Families

## Overview

This note models the **RPC method-family catalog** of the OpenClaw Gateway WebSocket protocol — the public WS methods a client invokes over the req/res/event envelope, grouped into the source's accordion families (system/identity, models/usage, channels, messaging, talk/TTS, secrets/config/update, agent/workspace, session control, device + node pairing, approval families, automation/skills/tools). It mirrors the "Common RPC method families" section of the `gateway/protocol` page. The companion event families, node-helper / task-ledger / operator-helper RPCs, `models.list` views, exec approvals, and agent delivery fallback are split into the sibling [oc_gateway_protocol_events_helpers](oc_gateway_protocol_events_helpers.md). Transport/framing is in `oc_gateway_protocol_transport`, role/scope in `oc_gateway_protocol_roles_scopes`, auth/pairing in `oc_gateway_protocol_auth_pairing`. The method list is **not a generated dump**: `hello-ok.features.methods` is a *conservative discovery list* from `src/gateway/server-methods-list.ts` plus loaded plugin/channel exports — "feature discovery, not a full enumeration of `src/gateway/server-methods/*.ts`."

## RPC Method Families

### System and identity

- `health` returns the cached or freshly probed gateway health snapshot.
- `diagnostics.stability` returns the bounded diagnostic stability recorder (operational metadata only — event names, counts, byte sizes, memory readings, queue/session state, channel/plugin names, session ids; **not** chat text, webhook/raw bodies, tool outputs, tokens, cookies, or secrets). Requires operator read scope.
- `status` returns the `/status`-style summary (sensitive fields only for admin-scoped operators); `gateway.identity.get` returns the gateway device identity used by relay/pairing.
- `system-presence` returns the presence snapshot for connected operator/node devices; `system-event` appends a system event and can update/broadcast presence context.
- `last-heartbeat` returns the latest persisted heartbeat event; `set-heartbeats` toggles heartbeat processing.

### Models and usage

- `models.list` returns the runtime-allowed model catalog (views below); `usage.status` returns provider usage windows / remaining quota; `usage.cost` returns aggregated cost summaries for a date range (`agentId`, or `agentScope: "all"` to aggregate).
- `doctor.memory.status` returns vector-memory / cached embedding readiness (`{ "probe": true }` / `{ "deep": true }` for a live ping); `doctor.memory.dreamDiary`, `doctor.memory.backfillDreamDiary`, `doctor.memory.resetDreamDiary`, `doctor.memory.resetGroundedShortTerm`, `doctor.memory.repairDreamingArtifacts`, `doctor.memory.dedupeDreamDiary` accept optional `{ "agentId": "agent-id" }`; `doctor.memory.remHarness` returns a bounded read-only REM harness preview (`operator.read`).
- `sessions.usage` returns per-session usage summaries (`agentId` or `agentScope: "all"`); `sessions.usage.timeseries` and `sessions.usage.logs` return timeseries usage and usage log entries for one session.

### Channels and login helpers

- `channels.status` returns built-in + bundled channel/plugin status summaries; `channels.logout` logs out a channel/account where supported by the channel.
- `web.login.start` / `web.login.wait` start/wait for a QR/web login flow for the current QR-capable web channel provider.
- `push.test` sends a test APNs push to a registered iOS node; `voicewake.get` / `voicewake.set` return/update wake-word triggers (set broadcasts the change).

### Messaging and logs

- `send` is the direct outbound-delivery RPC for channel/account/thread-targeted sends outside the chat runner; `logs.tail` returns the gateway file-log tail with cursor/limit and max-byte controls.

### Talk and TTS

- `talk.catalog` returns the read-only Talk provider catalog (provider ids, labels, state, model/voice ids, modes, transports, brain strategies, realtime flags) without secrets; `talk.config` returns the effective Talk config (`includeSecrets` requires `operator.talk.secrets` or `operator.admin`).
- `talk.session.create` creates a Gateway-owned session (`realtime/gateway-relay`, `transcription/gateway-relay`, `stt-tts/managed-room`; unscoped `sessionKey` and `brain: "direct-tools"` need `operator.admin`); `talk.session.join`, `talk.session.appendAudio`, `talk.session.startTurn`, `talk.session.endTurn`, `talk.session.cancelTurn`, `talk.session.cancelOutput`, `talk.session.submitToolResult`, `talk.session.steer`, `talk.session.close` drive managed-room/relay turn+tool lifecycle.
- `talk.mode` sets/broadcasts the Talk mode; `talk.client.create`, `talk.client.toolCall`, `talk.client.steer` manage client-owned realtime sessions (`webrtc` / `provider-websocket`) while the Gateway owns config/credentials/policy (first `talk.client.toolCall` tool is `openclaw_agent_consult`).
- `talk.event` is the single Talk event channel (realtime, transcription, STT/TTS, managed-room, telephony, meeting adapters); `talk.speak` synthesizes speech via the active provider.
- `tts.status`, `tts.providers`, `tts.enable`, `tts.disable`, `tts.setProvider`, `tts.convert` manage TTS state, inventory, prefs, and one-shot conversion.

### Secrets, config, update, and wizard

- `secrets.reload` re-resolves active SecretRefs and swaps runtime secret state only on full success; `secrets.resolve` resolves command-target secret assignments.
- `config.get` returns the config snapshot and hash; `config.set` writes a validated payload; `config.patch` merges a partial update (destructive array replacement needs the path in `replacePaths`; nested arrays use `[]` paths like `agents.list[].skills`); `config.apply` validates + replaces the full payload.
- `config.schema` returns the live config schema payload (schema, `uiHints`, version, generation metadata); `config.schema.lookup` returns a path-scoped lookup (normalized path, shallow schema node, matched hint + `hintPath`, optional `reloadKind` ∈ `restart`/`hot`/`none`).
- `update.run` runs the update flow and schedules a restart only on success; control-plane package-manager / git-checkout updates use a detached managed-service handoff (`result.reason: "managed-service-handoff-started"`, `handoff.status: "started"`; failures return `managed-service-handoff-unavailable` or `managed-service-handoff-failed`). `update.status` returns the latest restart sentinel + post-restart running version.
- `wizard.start`, `wizard.next`, `wizard.status`, `wizard.cancel` expose the onboarding wizard over WS RPC.

### Agent and workspace helpers

- `agents.list` returns configured agent entries (effective model + runtime metadata); `agents.create`, `agents.update`, `agents.delete` manage records/workspace wiring; `agents.files.list`, `agents.files.get`, `agents.files.set` manage bootstrap workspace files.
- `tasks.list`, `tasks.get`, `tasks.cancel` expose the Gateway task ledger (detailed below).
- `artifacts.list`, `artifacts.get`, `artifacts.download` expose transcript-derived artifact summaries/downloads for an explicit `sessionKey`, `runId`, or `taskId` scope (unsafe/local URL sources return unsupported downloads).
- `environments.list` / `environments.status` expose read-only Gateway-local + node environment discovery; `agent.identity.get` returns the effective assistant identity; `agent.wait` waits for a run to finish and returns the terminal snapshot.

### Session control

- `sessions.list` returns the session index (per-row `agentRuntime` when configured); `sessions.subscribe`/`sessions.unsubscribe` and `sessions.messages.subscribe`/`sessions.messages.unsubscribe` toggle session and transcript event subscriptions.
- `sessions.preview`, `sessions.describe`, `sessions.resolve`, `sessions.create`, `sessions.send`, `sessions.steer` (interrupt-and-steer), `sessions.abort`, `sessions.patch`, `sessions.reset`, `sessions.delete`, `sessions.compact`, and `sessions.get` cover session preview/resolution/creation/maintenance/stored-row reads; `sessions.abort` accepts `key` plus optional `runId`, or `runId` alone.
- Chat execution uses `chat.history`, `chat.send`, `chat.abort`, `chat.inject`. `chat.history` is display-normalized: inline directive tags, plain-text tool-call XML (`<tool_call>`, `<function_call>`, `<tool_calls>`, `<function_calls>`, truncated blocks), and leaked control tokens are stripped, pure silent-token rows (`NO_REPLY` / `no_reply`) omitted, oversized rows placeholder-replaced. `chat.message.get` is the bounded full-message reader for one visible transcript entry.

### Device pairing and device tokens

- `device.pair.list` returns pending and approved paired devices; `device.pair.approve`, `device.pair.reject`, and `device.pair.remove` manage device-pairing records.
- `device.token.rotate` and `device.token.revoke` rotate/revoke a paired device token within its approved role and caller scope bounds. (Detailed in `oc_gateway_protocol_auth_pairing`.)

### Node pairing, invoke, and pending work

- `node.pair.request`, `node.pair.list`, `node.pair.approve`, `node.pair.reject`, `node.pair.remove`, `node.pair.verify` cover node pairing and bootstrap verification.
- `node.list` / `node.describe` return known/connected node state; `node.rename` updates a paired node label; `node.invoke` forwards a command to a connected node; `node.invoke.result` returns its result; `node.event` carries node-originated events back into the gateway.
- `node.pending.pull` / `node.pending.ack` are the connected-node queue APIs; `node.pending.enqueue` / `node.pending.drain` manage durable pending work for offline nodes.

### Approval families

- `exec.approval.request`, `exec.approval.get`, `exec.approval.list`, `exec.approval.resolve` cover one-shot exec approval requests plus pending lookup/replay; `exec.approval.waitDecision` waits on one pending approval and returns the final decision (or `null` on timeout).
- `exec.approvals.get` / `exec.approvals.set` manage gateway exec approval policy snapshots; `exec.approvals.node.get` / `exec.approvals.node.set` manage node-local policy via node relay commands.
- `plugin.approval.request`, `plugin.approval.list`, `plugin.approval.waitDecision`, `plugin.approval.resolve` cover plugin-defined approval flows.

### Automation, skills, and tools

- Automation: `wake` schedules an immediate or next-heartbeat wake text injection; `cron.get`, `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`, `cron.run`, and `cron.runs` manage scheduled work. `cron.run` is an enqueue-style RPC (read the returned `runId` and poll `cron.runs`, which accepts an optional non-empty `runId` filter).
- Skills and tools: `commands.list`, `skills.*`, `tools.catalog`, `tools.effective`, `tools.invoke` (the operator-helper detail for these is in the [events-and-helpers sibling](oc_gateway_protocol_events_helpers.md)).

**Source**: OpenClaw documentation — `gateway/protocol` (mirror `inbox/openclaw_docs/gateway/protocol.md`)
**Last Updated**: 2026-06-22
**Status**: Active
