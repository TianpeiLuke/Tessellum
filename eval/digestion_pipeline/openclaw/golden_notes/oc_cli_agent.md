---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - agent
keywords:
  - openclaw agent command
  - run agent turn cli
  - session selector session-key
  - local embedded fallback
  - gateway timeout fallback
  - json deliver deliverystatus
  - model thinking override
  - chat.abort sigterm
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/agent
access_control_group: ["general"]
---

# OpenClaw — Running One Agent Turn with `openclaw agent`

## Overview

This note is the procedure for `openclaw agent`, the CLI command that runs a single agent turn via the Gateway (or embedded with `--local`). It mirrors the `cli/agent` source page: the session selectors you must supply, the full option surface, the worked examples, the operational Notes (Gateway→embedded fallback, session-key scoping, `--json` stdout discipline, SIGTERM/`chat.abort` interrupt handling, and SecretRef marker persistence), and the `--json --deliver` `deliveryStatus` response shape. It is the scripted-invocation counterpart to managing agents (`openclaw agents`) and the ACP bridge (`openclaw acp`).

## Command and Session Selectors

`openclaw agent` runs an agent turn via the Gateway; use `--local` for embedded execution, and use `--agent <id>` to target a configured agent directly. You must pass at least one session selector — `--to <dest>`, `--session-key <key>`, `--session-id <id>`, or `--agent <id>`. The source page also cross-links the in-agent **Agent send tool** (`/tools/agent-send`) as the tool-side counterpart of this CLI command.

## Options

The full option surface from the source page:

- `-m, --message <text>`: required message body
- `-t, --to <dest>`: recipient used to derive the session key
- `--session-key <key>`: explicit session key to use for routing
- `--session-id <id>`: explicit session id
- `--agent <id>`: agent id; overrides routing bindings
- `--model <id>`: model override for this run (`provider/model` or model id)
- `--thinking <level>`: agent thinking level (`off`, `minimal`, `low`, `medium`, `high`, plus provider-supported custom levels such as `xhigh`, `adaptive`, or `max`)
- `--verbose <on|off>`: persist verbose level for the session
- `--channel <channel>`: delivery channel; omit to use the main session channel
- `--reply-to <target>`: delivery target override
- `--reply-channel <channel>`: delivery channel override
- `--reply-account <id>`: delivery account override
- `--local`: run the embedded agent directly (after plugin registry preload)
- `--deliver`: send the reply back to the selected channel/target
- `--timeout <seconds>`: override agent timeout (default 600 or config value)
- `--json`: output JSON

## Examples

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --agent ops --model openai/gpt-5.4 --message "Summarize logs"
openclaw agent --session-key agent:ops:incident-42 --message "Summarize status"
openclaw agent --agent ops --session-key incident-42 --message "Summarize status"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
openclaw agent --agent ops --message "Run locally" --local
```

## Notes — Execution Mode, Fallback, and Routing

Gateway mode falls back to the embedded agent when the Gateway request fails; use `--local` to force embedded execution up front. `--local` still preloads the plugin registry first, so plugin-provided providers, tools, and channels stay available during embedded runs. `--local` and embedded fallback runs are treated as one-shot runs: bundled MCP loopback resources and warm Claude stdio sessions opened for that local process are retired after the reply, so scripted invocations do not keep local child processes alive. Gateway-backed runs leave Gateway-owned MCP loopback resources under the running Gateway process; older clients may still send the historical cleanup flag, but the Gateway accepts it as a compatibility no-op.

`--channel`, `--reply-channel`, and `--reply-account` affect reply delivery, not session routing. `--session-key` selects an explicit session key: agent-prefixed keys must use `agent:<agent-id>:<session-key>`, and `--agent` must match the key's agent id when both are provided. Bare non-sentinel keys are scoped to `--agent` when supplied, or to the configured default agent otherwise; for example, `--agent ops --session-key incident-42` routes to `agent:ops:incident-42`. Literal `global` and `unknown` remain unscoped only when no `--agent` is supplied; in that case, embedded fallback and store ownership use the configured default agent.

## Notes — JSON Output, Interrupts, and Secret Markers

`--json` keeps stdout reserved for the JSON response: Gateway, plugin, and embedded-fallback diagnostics are routed to stderr so scripts can parse stdout directly. Embedded fallback JSON includes `meta.transport: "embedded"` and `meta.fallbackFrom: "gateway"` so scripts can distinguish fallback runs from Gateway runs. If the Gateway accepts an agent run but the CLI times out waiting for the final reply, embedded fallback uses a fresh explicit `gateway-fallback-*` session/run id and reports `meta.fallbackReason: "gateway_timeout"` plus the fallback session fields — this avoids racing the Gateway-owned transcript lock or silently replacing the original routed conversation session.

For Gateway-backed runs, `SIGTERM` and `SIGINT` interrupt the waiting CLI request; if the Gateway has already accepted the run, the CLI also sends `chat.abort` for that accepted run id before exiting. Local `--local` runs and embedded fallback runs receive the same abort signal but do not send `chat.abort`. If a duplicate `--run-id` reaches the Gateway while the original agent run is still active, the duplicate response reports `status: "in_flight"` and the non-JSON CLI prints a stderr diagnostic instead of an empty reply. For external cron/systemd wrappers, keep an outer hard-kill backstop such as `timeout -k 60 600 openclaw agent ...` so the supervisor can still reap the process if shutdown cannot drain. When this command triggers `models.json` regeneration, SecretRef-managed provider credentials are persisted as non-secret markers (for example env var names, `secretref-env:ENV_VAR_NAME`, or `secretref-managed`), not resolved secret plaintext; marker writes are source-authoritative, so OpenClaw persists markers from the active source config snapshot, not from resolved runtime secret values.

## JSON Delivery Status

When `--json --deliver` is used, the CLI JSON response may include a top-level `deliveryStatus` so scripts can distinguish delivered, suppressed, partial, and failed sends:

```json
{
  "payloads": [{ "text": "Report ready", "mediaUrl": null }],
  "meta": { "durationMs": 1200 },
  "deliveryStatus": {
    "requested": true,
    "attempted": true,
    "status": "sent",
    "succeeded": true,
    "resultCount": 1
  }
}
```

`deliveryStatus.status` is one of `sent`, `suppressed`, `partial_failed`, or `failed`. `suppressed` means delivery was intentionally not sent, for example a message-sending hook cancelled it or there was no visible result; it is still a terminal no-retry outcome. `partial_failed` means at least one payload was sent before a later payload failed. `failed` means no durable send completed or delivery preflight failed. Gateway-backed CLI responses also preserve the raw Gateway result shape, where the same object is available at `result.deliveryStatus`.

Common fields:

- `requested`: always `true` when the object is present.
- `attempted`: `true` after the durable send path ran; `false` for preflight failures or no visible payloads.
- `succeeded`: `true`, `false`, or `"partial"`; `"partial"` pairs with `status: "partial_failed"`.
- `reason`: a lowercase snake-case reason from durable delivery or preflight validation. Known reasons include `cancelled_by_message_sending_hook`, `no_visible_payload`, `no_visible_result`, `channel_resolved_to_internal`, `unknown_channel`, `invalid_delivery_target`, and `no_delivery_target`; failed durable sends may also report the failed stage. Treat unknown values as opaque because the set can expand.
- `resultCount`: number of channel send results when available.
- `sentBeforeError`: `true` when a partial failure sent at least one payload before the error.
- `error`: boolean `true` for failed or partial-failed sends.
- `errorMessage`: included only when an underlying delivery error message is captured. Preflight failures carry `error` and `reason` but no `errorMessage`.
- `payloadOutcomes`: optional per-payload results with `index`, `status`, `reason`, `resultCount`, `error`, `stage`, `sentBeforeError`, or hook metadata when available.

**Source**: OpenClaw documentation — `cli/agent` (mirror `inbox/openclaw_docs/cli/agent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
