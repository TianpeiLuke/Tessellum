---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - acp
keywords:
  - openclaw acp compatibility matrix
  - acp bridge capability contract
  - acp known limitations
  - acp protocol smoke testing
  - loadsession partial replay
  - per-session mcpservers unsupported
  - session lineage metadata
  - session_info_update usage_update
topics:
  - OpenClaw
  - ACP Bridge Compatibility
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/cli/acp
access_control_group: ["general"]
---

# OpenClaw — ACP Bridge Compatibility Contract (Matrix, Limitations, Smoke-Test Ledger)

## Overview

This note models the capability **contract** of the `openclaw acp` Gateway-backed ACP bridge: which Agent Client Protocol (ACP) areas the bridge implements fully, which it supports only partially, and which it explicitly rejects — plus the Known Limitations that bound the "Partial" behaviors and the protocol smoke-test ledger that proves bridge correctness. It mirrors the `Compatibility Matrix`, `Known Limitations`, and `Protocol smoke testing` (ledger shape) sections of the `cli/acp` source page. The operational how-to of running the bridge (usage, debug client, `acpx`/Zed setup, options) lives in the sibling procedure note `oc_cli_acp_bridge`; this note is the ACP↔Gateway capability ledger only.

## Compatibility Matrix

The matrix maps each ACP area to one of three statuses — **Implemented**, **Partial**, or **Unsupported** — with the source's per-row notes preserved verbatim where load-bearing.

| ACP area | Status | Notes |
| --- | --- | --- |
| `initialize`, `newSession`, `prompt`, `cancel` | Implemented | Core bridge flow over stdio to Gateway chat/send + abort. |
| `listSessions`, slash commands | Implemented | Session list works against Gateway session state with bounded cursor pagination and `cwd` filtering where Gateway session rows carry workspace metadata; commands are advertised via `available_commands_update`. |
| Session lineage metadata | Implemented | Session listings and session info snapshots include OpenClaw parent and child lineage in `_meta` so ACP clients can render subagent graphs without private Gateway side channels. |
| `resumeSession`, `closeSession` | Implemented | Resume rebinds an ACP session to an existing Gateway session without replaying history. Close cancels active bridge work, resolves pending prompts as cancelled, and releases bridge session state. |
| `loadSession` | Partial | Rebinds the ACP session to a Gateway session key and replays ACP event-ledger history for bridge-created sessions. Older/no-ledger sessions fall back to stored user/assistant text. |
| Prompt content (`text`, embedded `resource`, images) | Partial | Text/resources are flattened into chat input; images become Gateway attachments. |
| Session modes | Partial | `session/set_mode` is supported and the bridge exposes initial Gateway-backed session controls for thought level, tool verbosity, reasoning, usage detail, and elevated actions. Broader ACP-native mode/config surfaces are still out of scope. |
| Session info and usage updates | Partial | The bridge emits `session_info_update` and best-effort `usage_update` notifications from cached Gateway session snapshots. Usage is approximate and only sent when Gateway token totals are marked fresh. |
| Tool streaming | Partial | `tool_call` / `tool_call_update` events include raw I/O, text content, and best-effort file locations when Gateway tool args/results expose them. Embedded terminals and richer diff-native output are still not exposed. |
| Exec approvals | Partial | Gateway exec approval prompts during active ACP prompt turns are relayed to the ACP client with `session/request_permission`. |
| Per-session MCP servers (`mcpServers`) | Unsupported | Bridge mode rejects per-session MCP server requests. Configure MCP on the OpenClaw gateway or agent instead. |
| Client filesystem methods (`fs/read_text_file`, `fs/write_text_file`) | Unsupported | The bridge does not call ACP client filesystem methods. |
| Client terminal methods (`terminal/*`) | Unsupported | The bridge does not create ACP client terminals or stream terminal ids through tool calls. |
| Session plans / thought streaming | Unsupported | The bridge currently emits output text and tool status, not ACP plan or thought updates. |

The Implemented rows form the bridge's stable core: full session create/prompt/cancel over stdio, session listing with cursor pagination + `cwd` filtering, parent/child lineage in `_meta`, and resume/close. The Partial rows are best-effort approximations bounded by the Known Limitations below. The Unsupported rows are the bridge's hard boundary versus a fully ACP-native runtime — per-session `mcpServers`, ACP client filesystem methods, ACP client terminals, and ACP plan/thought streaming.

## Known Limitations

The Known Limitations qualify the "Partial" matrix rows — they describe exactly where each best-effort behavior degrades or is scoped:

- `loadSession` can replay complete ACP event-ledger history only for bridge-created sessions. Older/no-ledger sessions still use transcript fallback and do not reconstruct historic tool calls or system notices.
- If multiple ACP clients share the same Gateway session key, event and cancel routing are best-effort rather than strictly isolated per client. Prefer the default isolated `acp-bridge:<uuid>` sessions when you need clean editor-local turns.
- Gateway stop states are translated into ACP stop reasons, but that mapping is less expressive than a fully ACP-native runtime.
- Initial session controls currently surface a focused subset of Gateway knobs: thought level, tool verbosity, reasoning, usage detail, and elevated actions. Model selection and exec-host controls are not yet exposed as ACP config options.
- `session_info_update` and `usage_update` are derived from Gateway session snapshots, not live ACP-native runtime accounting. Usage is approximate, carries no cost data, and is only emitted when the Gateway marks total token data as fresh.
- Tool follow-along data is best-effort. The bridge can surface file paths that appear in known tool args/results, but it does not yet emit ACP terminals or structured file diffs.
- Exec approval relay is scoped to the active ACP prompt turn; approvals from other Gateway sessions are ignored.

## Protocol Smoke Testing (Capability Ledger)

The contract is proven by a protocol-level smoke test, not by trusting the matrix. For protocol-level debugging, start a Gateway with isolated state and drive `openclaw acp` over stdio with an ACP JSON-RPC client. The smoke test must cover `initialize`, `session/new`, `session/list` with an absolute `cwd`, `session/resume`, `session/close`, duplicate close, and missing resume.

The proof should include the advertised lifecycle capabilities, a Gateway-backed session row, update notifications, and the Gateway `sessions.list` log. The smoke-test ledger has this shape:

```json
{
  "initialize": {
    "protocolVersion": 1,
    "agentCapabilities": {
      "sessionCapabilities": {
        "list": {},
        "resume": {},
        "close": {}
      }
    }
  },
  "listSessions": {
    "sessions": [
      {
        "sessionId": "agent:main:acp-smoke",
        "cwd": "/path/to/workspace",
        "_meta": {
          "sessionKey": "agent:main:acp-smoke",
          "kind": "direct"
        }
      }
    ],
    "nextCursor": null
  },
  "notifications": ["session_info_update", "available_commands_update", "usage_update"],
  "gatewayLogTail": ["[gateway] ready", "[ws] ⇄ res ✓ sessions.list 305ms"]
}
```

The ledger ties directly back to the matrix: `protocolVersion: 1` plus the `sessionCapabilities` (`list` / `resume` / `close`) are the advertised lifecycle capabilities that prove the Implemented rows; the `listSessions` row carries the `_meta.sessionKey` + `kind` lineage metadata; and the `notifications` array is the live evidence of the Partial `session_info_update` / `usage_update` rows alongside the Implemented `available_commands_update` slash-command advertisement. Crucially, the source warns: avoid using `openclaw gateway call sessions.list` as the only ACP proof — that CLI path may request a fresh-token operator scope upgrade; ACP bridge correctness is proven by ACP stdio frames plus the Gateway `sessions.list` log (the `gatewayLogTail` entry).

**Source**: OpenClaw documentation — `cli/acp` (mirror `inbox/openclaw_docs/cli/acp.md`), Compatibility Matrix + Known Limitations + Protocol smoke testing
**Last Updated**: 2026-06-22
**Status**: Active
