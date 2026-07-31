---
title: Sub-Plan cl01 — OpenClaw Docs: CLI (acp, agent, agents, approvals, backup, browser, channels)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/acp", "cli/agent", "cli/agents", "cli/approvals", "cli/backup", "cli/browser", "cli/channels"]
---

# Sub-Plan cl01: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*` prefix), format (YAML field order + body
> structure + density caps), dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), the
> 9-GATE per phase, the cross-reference link set, and the entry-point/series-wiring decisions are ALL
> inherited verbatim from the master. This file re-measures its 7 assigned pages, maps every H2/H3 to a

## Scope

The first 7 of the 58 `cli/*` reference pages — the highest-traffic operational CLI surface for driving an
OpenClaw Gateway from the terminal: `openclaw acp` (the ACP bridge for IDE integrations), `openclaw agent`
(one scripted agent turn via the Gateway), `openclaw agents` (manage isolated agents — workspaces, auth,
routing bindings, identity), `openclaw approvals`/`exec-policy` (edit exec approvals on local/gateway/node
hosts), `openclaw backup` (local state backup archives), `openclaw browser` (browser control surface +
actions), and `openclaw channels` (chat channel accounts, status, login/logout). **Priority P1 (Phase A)** —
these CLI commands are the operational vocabulary the gateway, concepts, tools, and channels sub-plans
reference. The code-side counterparts (`repo_openclaw_cli_wizard`, `repo_openclaw_agents`,
`repo_openclaw_gateway`, `repo_openclaw_channels`, `repo_openclaw_security`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 8,667 measured words. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| acp | cli/acp | 2,132 | 12 | 13 | 1 | procedure (split: bridge setup vs ACP compatibility/limitations model) |
| agent | cli/agent | 1,062 | 4 | 5 | 0 | procedure |
| agents | cli/agents | 960 | 9 | 6 | 9 | procedure |
| approvals | cli/approvals | 860 | 8 | 8 | 0 | procedure |
| backup | cli/backup | 737 | 4 | 5 | 0 | procedure |
| browser | cli/browser | 1,721 | 15 | 13 | 0 | procedure |
| channels | cli/channels | 1,195 | 5 | 8 | 0 | procedure |

(Measured via `wc -w` on each mirror file; Code = `grep -c '```' / 2`; H2/H3 = `grep -nE '^## '` / `'^### '`.)

## Content Strategy

- **Prioritize**: `agents` routing bindings (the `--bind <channel>[:account]` model every multi-agent setup
  uses), `approvals`/`exec-policy` precedence (host approvals file vs requested `tools.exec.*`), `browser`
  action verbs + profile model (managed / user-MCP / CDP), and the `acp` bridge-vs-harness distinction (a
  page the docs themselves flag as commonly confused). These are the most-cross-referenced CLI surfaces.
- **Split**: only `acp.md` (2,132w, 13 H2, mixed BB). It mixes a setup/usage procedure (run the bridge,
  point an IDE/`acpx` at it, Zed setup, session mapping, options) with a distinct ACP↔Gateway capability
  CONTRACT (Compatibility Matrix + Known Limitations + the protocol smoke-test ledger) that is a model BB.
  Split into a procedure note + a model note (see Split Decisions). All other pages stay 1 note (each ≤2,132w,
  single procedure BB).
- **Link-out (do not duplicate)**: ACP-harness/`acpx` deep config, ACP Agents, and `openclaw mcp serve` →
  `tools/acp-agents*` (to01) + `cli/mcp` (cl04); exec-approvals concept/tool deep-dive → `tools/exec-approvals`
  (to03); browser tool API + SSRF/CDP troubleshooting → `tools/browser` (to01/to02); per-channel setup guides
  → `channels/*` (ch01–06); multi-agent routing + agent-workspace concepts → `concepts/multi-agent`,
  `concepts/agent-workspace`, `concepts/agent`, `concepts/session` (co01–07); gateway config + remote/auth →
  `gateway/configuration`, `gateway/config-agents`, `gateway/remote`, `gateway/tailscale`, `gateway/security`
  (gw01–06); reset/uninstall → `cli/reset`/`cli/uninstall` (cl06/cl08). Terms link `term_openclaw`,
  `term_acp_agent_client_protocol`, `term_mcp`, etc. — never inline a definition.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_acp_bridge.md` | procedure | acp.md: What this is not, Usage, ACP client (debug), Protocol smoke testing, How to use this, Selecting agents, Use from acpx, Zed editor setup, Session mapping, Options (+ acp client options) | 650 | Running `openclaw acp`, the Gateway-backed ACP bridge for IDEs: bridge-vs-harness distinction, usage + remote-Gateway flags, the debug ACP client, agent selection by session key, `acpx`/Zed setup, session mapping, and all bridge/`acp client` options. |
| 2 | `oc_cli_acp_compatibility.md` | model | acp.md: Compatibility Matrix, Known Limitations, Protocol smoke testing (ledger shape) | 550 | The ACP↔Gateway bridge capability contract: the Compatibility Matrix (implemented / partial / unsupported ACP areas), the Known Limitations, and the smoke-test capability ledger that proves bridge correctness. |
| 3 | `oc_cli_agent.md` | procedure | agent.md: (intro/selectors), Options, Examples, Notes, JSON delivery status | 500 | Running one agent turn via the Gateway with `openclaw agent`: session selectors, message/model/thinking/reply options, embedded `--local` fallback semantics, and the `--json --deliver` `deliveryStatus` shape. |
| 4 | `oc_cli_agents.md` | procedure | agents.md: (intro), Examples, Routing bindings (+ `--bind` format, Binding scope behavior), Command surface (all subcommands), Identity files, Set identity | 600 | Managing isolated agents with `openclaw agents`: list/add/delete, routing bindings (`--bind <channel>[:account]`, scope/upgrade behavior), the full subcommand surface, identity files, and `set-identity`. |
| 5 | `oc_cli_approvals.md` | procedure | approvals.md: (intro), `openclaw exec-policy`, Common commands, Replace approvals from a file, "Never prompt"/YOLO example, Allowlist helpers, Common options, Notes | 600 | Editing exec approvals from the CLI with `openclaw approvals`/`exec-policy`: host targeting (local/gateway/node), the host-approvals-file vs requested `tools.exec.*` precedence, replace-from-file, YOLO preset, and allowlist helpers. |
| 6 | `oc_cli_backup.md` | procedure | backup.md: (intro/examples), Notes, What gets backed up, Invalid config behavior, Size and performance | 450 | Creating local backup archives with `openclaw backup`: what's archived (state, config, auth profiles, credentials, sessions, optional workspaces), the manifest, verify/dry-run/only-config flags, invalid-config recovery, and size/performance. |
| 7 | `oc_cli_browser.md` | procedure | browser.md: Common flags, Quick start, Quick troubleshooting, Lifecycle, If the command is missing, Profiles, Tabs, Snapshot/screenshot/actions, State and storage, Debugging, Existing Chrome via MCP, Remote browser control (node host proxy) | 700 | Driving OpenClaw's browser control surface with `openclaw browser`: lifecycle + doctor, profiles (managed / `user` Chrome-MCP / CDP), tabs, snapshot/screenshot/ref-based actions, state emulation + cookies/storage, debugging, existing-Chrome via MCP, and remote node-host proxying. |
| 8 | `oc_cli_channels.md` | procedure | channels.md: (intro), Common commands, Status/capabilities/resolve/logs, Add/remove accounts, Login and logout, Troubleshooting, Capabilities probe, Resolve names to IDs | 600 | Managing chat-channel accounts with `openclaw channels`: list/status/capabilities/resolve/logs, add/remove accounts (per-channel flags + interactive bind), interactive login/logout, capability probes, and name→ID resolution. |

Filename rule applied: `oc_` + slug with `/` and `-` → `_`. `cli/acp` splits, so the two halves take aspect
suffixes (`oc_cli_acp_bridge`, `oc_cli_acp_compatibility`); all other CLI pages map 1:1 (e.g. `cli/agents` →
`oc_cli_agents.md`). One BB per note.

## Section Coverage Map

```
acp.md (13 H2 / 1 H3)
├── (lead paragraphs: bridge purpose, mcp serve pointer) → note 1 (oc_cli_acp_bridge)
├── What this is not ─────────────────────────────────── → note 1
├── Compatibility Matrix ─────────────────────────────── → note 2 (oc_cli_acp_compatibility)
├── Known Limitations ────────────────────────────────── → note 2
├── Usage ────────────────────────────────────────────── → note 1
├── ACP client (debug) ───────────────────────────────── → note 1
├── Protocol smoke testing ───────────────────────────── → note 2 (ledger/capabilities) + note 1 (how-to driving) [primary: note 2]
├── How to use this ──────────────────────────────────── → note 1
├── Selecting agents ─────────────────────────────────── → note 1
├── Use from `acpx` (Codex, Claude, …) ───────────────── → note 1
├── Zed editor setup ─────────────────────────────────── → note 1
├── Session mapping ──────────────────────────────────── → note 1
├── Options ──────────────────────────────────────────── → note 1
│   └── ### `acp client` options ─────────────────────── → note 1
└── Related ──────────────────────────────────────────── → notes 1+2 References

agent.md (5 H2)
├── (lead: run agent turn, selectors) ────────────────── → note 3 (oc_cli_agent)
├── Options ──────────────────────────────────────────── → note 3
├── Examples ─────────────────────────────────────────── → note 3
├── Notes ────────────────────────────────────────────── → note 3
├── JSON delivery status ─────────────────────────────── → note 3
└── Related ──────────────────────────────────────────── → note 3 References

agents.md (6 H2 / 9 H3)
├── (lead: manage isolated agents) ───────────────────── → note 4 (oc_cli_agents)
├── Examples ─────────────────────────────────────────── → note 4
├── Routing bindings ─────────────────────────────────── → note 4
│   ├── ### `--bind` format ──────────────────────────── → note 4
│   └── ### Binding scope behavior ───────────────────── → note 4
├── Command surface ──────────────────────────────────── → note 4
│   └── ### agents / list / add / bindings / bind /
│       unbind / delete (7 H3) ───────────────────────── → note 4
├── Identity files ───────────────────────────────────── → note 4
├── Set identity ─────────────────────────────────────── → note 4
└── Related ──────────────────────────────────────────── → note 4 References

approvals.md (8 H2)
├── (lead: manage exec approvals) ────────────────────── → note 5 (oc_cli_approvals)
├── `openclaw exec-policy` ───────────────────────────── → note 5
├── Common commands ──────────────────────────────────── → note 5
├── Replace approvals from a file ────────────────────── → note 5
├── "Never prompt" / YOLO example ────────────────────── → note 5
├── Allowlist helpers ────────────────────────────────── → note 5
├── Common options ───────────────────────────────────── → note 5
├── Notes ────────────────────────────────────────────── → note 5
└── Related ──────────────────────────────────────────── → note 5 References

backup.md (5 H2)
├── (lead + examples) ────────────────────────────────── → note 6 (oc_cli_backup)
├── Notes ────────────────────────────────────────────── → note 6
├── What gets backed up ──────────────────────────────── → note 6
├── Invalid config behavior ──────────────────────────── → note 6
├── Size and performance ─────────────────────────────── → note 6
└── Related ──────────────────────────────────────────── → note 6 References

browser.md (13 H2)
├── (lead: browser control surface) ──────────────────── → note 7 (oc_cli_browser)
├── Common flags ─────────────────────────────────────── → note 7
├── Quick start (local) ──────────────────────────────── → note 7
├── Quick troubleshooting ────────────────────────────── → note 7
├── Lifecycle ────────────────────────────────────────── → note 7
├── If the command is missing ────────────────────────── → note 7
├── Profiles ─────────────────────────────────────────── → note 7
├── Tabs ─────────────────────────────────────────────── → note 7
├── Snapshot / screenshot / actions ──────────────────── → note 7
├── State and storage ────────────────────────────────── → note 7
├── Debugging ────────────────────────────────────────── → note 7
├── Existing Chrome via MCP ──────────────────────────── → note 7
├── Remote browser control (node host proxy) ─────────── → note 7
└── Related ──────────────────────────────────────────── → note 7 References

channels.md (8 H2)
├── (lead: manage channel accounts) ──────────────────── → note 8 (oc_cli_channels)
├── Common commands ──────────────────────────────────── → note 8
├── Status / capabilities / resolve / logs ───────────── → note 8
├── Add / remove accounts ────────────────────────────── → note 8
├── Login and logout (interactive) ───────────────────── → note 8
├── Troubleshooting ──────────────────────────────────── → note 8
├── Capabilities probe ───────────────────────────────── → note 8
├── Resolve names to IDs ─────────────────────────────── → note 8
└── Related ──────────────────────────────────────────── → note 8 References
```
No orphaned sections. Every page's `## Related` becomes that note's `## References`; deep-dive pointers
(`tools/*`, `concepts/*`, `gateway/*`, `channels/*`, `nodes`, `cli/mcp`) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| acp.md (2,132w, 13 H2 / 1 H3, mixed BB) | notes 1 (`oc_cli_acp_bridge`, procedure) + 2 (`oc_cli_acp_compatibility`, model) | The page mixes a setup/usage PROCEDURE (run the bridge, debug client, acpx/Zed setup, session mapping, options) with a distinct ACP↔Gateway capability CONTRACT/MODEL (the Compatibility Matrix of implemented/partial/unsupported ACP methods, Known Limitations, and the smoke-test capability ledger). One BB per note ⇒ split. Keeps each ≤700w and ≤6 code blocks. |
| agent / agents / approvals / backup / browser / channels | 1 note each | Each is a single-command reference under the 2,500w cap with one procedure BB; no split needed (browser at 1,721w is the largest and stays one focused command-reference note). |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (8,667 words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×7 (notes 1, 3, 4, 5, 6, 7, 8) · model ×1 (note 2 — the ACP compatibility/limitations contract).
- Est. digest words ~4,650 (avg ~580/note). 57 source code fences (`acp` 12, `browser` 15, `agents` 9,
  `approvals` 8, `channels` 5, `agent` 4, `backup` 4) distribute across the notes; each note keeps ≤6 by
  reproducing only representative command blocks (the acp split keeps the bridge note's many bash blocks ≤6
  and the JSON ledger in the model note).
- Cross-refs (LOCKED at xref-augment 2026-06-21, RAISED floors): each note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (≥5 EXISTING
  this series)" toward the 10-doc floor), PLUS relevant `repo_openclaw*`, each link with a per-link relevance

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21,
> exist yet → marked "(planned, this series)" and counted toward the 10-doc floor, but each note carries
> `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`, sibling → `oc_X.md`,
> other doc → `../<folder>/`, repo → `../../../areas/code_repos/`, snippet → `../../code_snippets/`,
> entry point → `../../../0_entry_points/`.

### oc_cli_acp_bridge (9t · 12s · 11d)

**Terms**
- [Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the IDE↔agent protocol; relevance: `openclaw acp` is the ACP server this bridge speaks over stdio.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product; relevance: the bridge forwards ACP work into an OpenClaw Gateway session.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the page explicitly contrasts `openclaw mcp serve` against the ACP bridge and rejects per-session `mcpServers`.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON-RPC 2.0 request/response framing; relevance: ACP frames (`initialize`/`session/new`/`prompt`/`cancel`) are JSON-RPC over stdio.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the bridge forwards prompts to the Gateway over WebSocket (`--url wss://…`).
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's coding agent; relevance: `acpx` can run Claude Code as an ACP client that drives the OpenClaw bridge.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Codex/Claude/Gemini harness family; relevance: the "Use from acpx" section targets these harnesses as ACP clients.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: each ACP session maps to a Gateway session key (`--session`/`--session-label`/`--reset-session`).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent-loop runtime; relevance: the page distinguishes the Gateway-backed bridge from an ACP-harness runtime (`/acp spawn`).

**Docs**
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — Claude Code MCP transport types (stdio/SSE/HTTP); relevance: closest existing analog of the bridge's stdio-to-WS transport split.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — MCP architecture in Claude Code; relevance: clarifies the `openclaw mcp serve` alternative the page points to.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting agent sessions for external clients; relevance: parallels the Gateway-backed session the bridge attaches IDEs to.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/token + network failure handling; relevance: analog for the bridge's `--token`/`--token-file` Gateway auth contract.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi's stdio JSON-RPC protocol; relevance: direct analog of ACP-over-stdio framing and capability negotiation.
- [pi_sessions](../pi/pi_sessions.md) — Pi session lifecycle; relevance: analog for ACP→Gateway session-key binding and resume semantics.
- [hermes_acp_editor_integration](../hermes_agent/hermes_acp_editor_integration.md) — Hermes ACP editor (Zed) integration; relevance: direct analog of the Zed `agent_servers` setup block.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP bridge internals; relevance: closest implementation analog of the bridge routing/session mapping.
- [oc_cli_acp_compatibility](oc_cli_acp_compatibility.md) — (planned, this series) the ACP↔Gateway capability contract; relevance: this bridge setup exercises that compatibility matrix.
- [oc_cli_agent](oc_cli_agent.md) — (planned, this series) `openclaw agent` one-shot turn; relevance: shares the agent-scoped session-key targeting model.
- [oc_cli_channels](oc_cli_channels.md) — (planned, this series) channel accounts; relevance: ACP sessions ultimately drive the same Gateway that channels feed.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — ACP manager/runtime + subagent spawn; relevance: implements the ACP server runtime behind `openclaw acp`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway WS endpoint; relevance: the WebSocket target the bridge forwards prompts into.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `openclaw` CLI dispatch; relevance: hosts the `acp` and `acp client` command surface.

**Snippets**
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP stdio server entry; relevance: the server `openclaw acp` runs.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — `initialize`/`newSession` translation; relevance: implements the bridge's session-create flow.
- [snippet_openclaw_acp_translator_prompt](../../code_snippets/snippet_openclaw_acp_translator_prompt.md) — `prompt` frame translation; relevance: forwards ACP prompts to Gateway chat.send.
- [snippet_openclaw_acp_translator_cancel](../../code_snippets/snippet_openclaw_acp_translator_cancel.md) — `cancel` translation; relevance: implements the bridge's cancel/abort path.
- [snippet_openclaw_acp_persistent_bindings](../../code_snippets/snippet_openclaw_acp_persistent_bindings.md) — persistent ACP session bindings; relevance: backs `--session`/`--session-label` reuse.
- [snippet_openclaw_acp_spawn_session_handoff](../../code_snippets/snippet_openclaw_acp_spawn_session_handoff.md) — ACP spawn/session handoff; relevance: clarifies bridge-vs-`/acp spawn` boundary the page warns about.
- [snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md) — ACP runtime registration; relevance: registers the bridge runtime with the manager.
- [snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md) — ACP spawn policy; relevance: governs bridge-session vs `/acp spawn` harness boundary.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: where `acp`/`acp client` register as commands.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: dispatches `openclaw acp` to its handler.
- [snippet_openclaw_gateway_server_startup_acp_prewarm](../../code_snippets/snippet_openclaw_gateway_server_startup_acp_prewarm.md) — Gateway ACP prewarm at startup; relevance: warms the Gateway-side ACP runtime the bridge connects to.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key parsing/scoping; relevance: implements `agent:<id>:<key>` mapping the bridge uses.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_acp_compatibility (8t · 11s · 10d)

**Terms**
- [Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the ACP method surface; relevance: the Compatibility Matrix maps every ACP area to implemented/partial/unsupported.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the contract is OpenClaw's ACP-bridge capability ledger.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC framing; relevance: the matrix rows are the `initialize`/`session.*`/`prompt`/`cancel` JSON-RPC methods.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: per-session `mcpServers` is the explicitly Unsupported area (bridge rejects it).
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `loadSession` replay / `resumeSession` rebinding are Partial/Implemented matrix rows.
- [WebSocket](../../term_dictionary/term_websocket.md) — Gateway transport; relevance: `session_info_update`/`usage_update` are derived from Gateway WS snapshots.
- [Subagent](../../term_dictionary/term_subagent.md) — child-agent lineage; relevance: session listings include parent/child lineage `_meta` so ACP clients render subagent graphs.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — full agent runtime; relevance: Known Limitations note the bridge is less expressive than an ACP-native runtime.

**Docs**
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — Pi RPC command surface; relevance: direct analog of an RPC-method capability table.
- [pi_rpc_events](../pi/pi_rpc_events.md) — Pi RPC event surface; relevance: analog for the `*_update` notification rows in the matrix.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi RPC protocol contract; relevance: analog of protocol-version/capability negotiation in the smoke-test ledger.
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — MCP transports; relevance: contextualizes the Unsupported per-session `mcpServers` row.
- [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — session list/resume/load API; relevance: analog for `listSessions`/`resumeSession`/`loadSession` matrix rows.
- [cc_sessions](../claude_code/cc_sessions.md) — session model; relevance: analog for session-info/usage update semantics.
- [hermes_acp_internals](../hermes_agent/hermes_acp_internals.md) — Hermes ACP internals; relevance: direct implementation analog of an ACP bridge's supported/unsupported surface.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle/resume; relevance: analog for the resume-vs-load distinction in the matrix.
- [oc_cli_acp_bridge](oc_cli_acp_bridge.md) — (planned, this series) the bridge procedure; relevance: the setup that exercises this contract.
- [oc_cli_agent](oc_cli_agent.md) — (planned, this series) one-shot turn; relevance: shares the chat.send/abort path the matrix's core rows wrap.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — ACP runtime contract + event ledger; relevance: implements the matrix's method-level behavior + smoke-test ledger.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway session state + exec-approval relay; relevance: backs the Partial "exec approvals" and "usage update" rows.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session-key + lineage backing; relevance: backs `listSessions` lineage `_meta` and `loadSession` replay.

**Snippets**
- [snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md) — ACP runtime capability contract; relevance: the code form of the Compatibility Matrix.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: backs `loadSession` event-ledger replay (Partial row).
- [snippet_openclaw_acp_manager_turn_stream](../../code_snippets/snippet_openclaw_acp_manager_turn_stream.md) — turn streaming; relevance: implements `tool_call`/`tool_call_update` streaming (Partial row).
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — exec-approval relay; relevance: implements `session/request_permission` (Partial exec-approvals row).
- [snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md) — session control apply; relevance: implements `session/set_mode` initial-controls (Partial row).
- [snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md) — translator rate limiting; relevance: governs best-effort usage/notification emission noted in Known Limitations.
- [snippet_openclaw_acp_manager_detached_runtime](../../code_snippets/snippet_openclaw_acp_manager_detached_runtime.md) — detached runtime mgmt; relevance: clarifies bridge-vs-harness runtime boundary in the matrix.
- [snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md) — `initialize`/`newSession`; relevance: the Implemented core-flow rows.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: backs lineage `_meta` for subagent graphs.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: backs `resumeSession`/`closeSession` row behavior.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — chat lifecycle persistence; relevance: backs the Gateway-snapshot-derived `session_info_update` row.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_agent (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw agent` runs one turn via the OpenClaw Gateway.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent-loop runtime; relevance: `--local` forces the embedded agent harness run.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway the turn runs through; relevance: Gateway mode falls back to embedded when the Gateway request fails.
- [Model Router](../../term_dictionary/term_model_router.md) — provider/model routing; relevance: `--model provider/model` overrides routing for the run.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `--session-key`/`--session-id`/`--to` derive the routed session.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation in a turn; relevance: the agent turn may invoke tools/MCP loopback resources retired after a one-shot run.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: bundled MCP loopback resources/warm stdio sessions are retired after the reply.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — provider failover; relevance: embedded fallback uses a fresh `gateway-fallback-*` session and reports `meta.fallbackReason`.

**Docs**
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI command reference; relevance: sibling-tool analog of a single agent-turn CLI command.
- [cc_cli_flags](../claude_code/cc_cli_flags.md) — Claude Code CLI flags; relevance: analog of the `--message`/`--model`/`--thinking`/`--json` flag surface.
- [cc_agent_sdk_message_types](../claude_code/cc_agent_sdk_message_types.md) — SDK message/result types; relevance: analog of the JSON response + `deliveryStatus` shape.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — scripted/background runs; relevance: analog of scripted `--json --deliver` invocation hygiene.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference; relevance: analog of a coding-agent one-shot CLI run.
- [hermes_cli_commands_session_ops](../hermes_agent/hermes_cli_commands_session_ops.md) — Hermes session-op CLI; relevance: analog of session-key-targeted CLI turns.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes provider fallback; relevance: direct analog of Gateway→embedded fallback semantics.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: analog of `--model provider/model` override routing.
- [oc_cli_agents](oc_cli_agents.md) — (planned, this series) manage isolated agents; relevance: `--agent <id>` targets agents created there.
- [oc_cli_acp_bridge](oc_cli_acp_bridge.md) — (planned, this series) ACP bridge; relevance: shares agent-scoped session-key targeting.
- [oc_cli_channels](oc_cli_channels.md) — (planned, this series) channels; relevance: `--reply-channel`/`--channel` deliver the turn's reply.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — embedded agent run + fallback; relevance: implements `--local` and Gateway-timeout fallback.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — chat.send/chat.abort/deliveryStatus; relevance: backs the Gateway-mode run and abort-on-SIGTERM path.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI command + JSON output; relevance: hosts `openclaw agent` and stdout-reserved JSON handling.

**Snippets**
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — Gateway chat.send; relevance: the handler the turn dispatches to.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — Gateway chat.abort; relevance: backs SIGTERM→`chat.abort` for accepted runs.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch; relevance: routes the run to the targeted agent/session.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error handling; relevance: backs `meta.fallbackReason: gateway_timeout`.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: backs `--model` override + provider fallback.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: governs repeated fallback attempts within a run.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: implements `--session-id`/`--session-key`/`--to` derivation.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — per-session model override; relevance: backs `--model` run override.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/delivery policy; relevance: backs `--deliver`/`deliveryStatus` outcomes.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP HTTP loopback; relevance: the bundled MCP loopback resources retired after a one-shot run.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: dispatches `openclaw agent` to its handler.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_agents (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw agents` manages isolated OpenClaw agents.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple isolated agents; relevance: isolated agents = workspaces + auth + routing, the page's core model.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — per-agent runtime; relevance: each agent is a workspace-scoped harness instance.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel transport; relevance: routing bindings pin inbound channel traffic to a specific agent.
- [Cap Routing](../../term_dictionary/term_cap_routing.md) — capability/channel→agent routing; relevance: `--bind <channel>[:account]` is the routing-binding mechanism.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credentials; relevance: auth seeding copies portable static profiles; OAuth refresh-tokens stay read-through from `main`.
- [Authentication](../../term_dictionary/term_authentication.md) — per-agent auth; relevance: `agents add` seeds auth profiles for the new agent.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — multi-platform account set; relevance: bindings span Telegram/Discord/etc. accounts (`--bind telegram:*`).
- [Subagent](../../term_dictionary/term_subagent.md) — child agents; relevance: identity/workspace scoping is the basis for subagent isolation.

**Docs**
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — create a Claude Code subagent; relevance: direct analog of `agents add` (isolated agent creation).
- [cc_forked_subagents](../claude_code/cc_forked_subagents.md) — forked/isolated subagents; relevance: analog of workspace + identity isolation per agent.
- [cc_subagent_configuration_reference](../claude_code/cc_subagent_configuration_reference.md) — subagent config fields; relevance: analog of `agents.list[]` identity/skills/model config.
- [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — subagent model; relevance: analog of the multi-agent isolation concept.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference; relevance: analog of an agent-management CLI surface.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — Hermes multi-agent profiles; relevance: direct analog of isolated agents + per-agent config.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes subagent delegation; relevance: analog of routing work to a specific agent.
- [hermes_webhooks_routing_delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — Hermes routing/delivery; relevance: analog of channel→agent routing bindings.
- [oc_cli_channels](oc_cli_channels.md) — (planned, this series) channel accounts; relevance: `channels add` can write the same routing bindings interactively.
- [oc_cli_agent](oc_cli_agent.md) — (planned, this series) one-shot turn; relevance: `--agent <id>` targets agents managed here.
- [oc_cli_acp_bridge](oc_cli_acp_bridge.md) — (planned, this series) ACP bridge; relevance: routes by agent-scoped session keys defined here.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent CRUD + bindings + identity; relevance: implements list/add/delete/bind/set-identity.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel bindings reference; relevance: backs `--bind <channel>[:account]` account resolution.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `agents` subcommand surface; relevance: hosts the full command surface.

**Snippets**
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding→agent routing; relevance: implements `--bind` resolution to an agent.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread/account binding policy; relevance: backs binding scope/upgrade behavior.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity fields; relevance: implements `set-identity`/`IDENTITY.md`.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope resolution; relevance: implements `--agent` default-agent scoping.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering; relevance: backs auth seeding (static vs OAuth read-through).
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth portability; relevance: backs "OAuth refresh-tokens stay read-through from main".
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: backs portable static profile copy on `agents add`.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — per-agent runtime config; relevance: backs `--workspace`/`--model`/`--agent-dir` add flags.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — subagent registry announce; relevance: backs agent registration/listing.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: defines the channel/account namespace bindings resolve against.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: where `agents` subcommands register.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_approvals (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw approvals`/`exec-policy` edit OpenClaw exec approvals.
- [Sandbox](../../term_dictionary/term_sandbox.md) — sandboxed exec; relevance: `host=auto` means "sandbox when available, otherwise gateway"; YOLO is about approvals not routing.
- [Access Control](../../term_dictionary/term_access_control.md) — allow/deny rules; relevance: allowlist add/remove + per-agent `*` scope are the page's core operation.
- [Authentication](../../term_dictionary/term_authentication.md) — node-RPC auth; relevance: `--node` targets use shared node-RPC `--token`/`--url`.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway host; relevance: `--gateway` targets the gateway host approvals file.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — SecretRef-managed config; relevance: requested `tools.exec.*` config can be SecretRef-managed.
- [Cron](../../term_dictionary/term_cron.md) — scheduled wrappers; relevance: external cron/systemd wrappers run approvals-gated exec commands.
- [Subagent](../../term_dictionary/term_subagent.md) — per-agent scope; relevance: `--agent <id>` scopes allowlist entries to an agent (default `*` = all agents).

**Docs**
- [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — permission modes; relevance: direct analog of exec-approval ask/security modes.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool permission rules; relevance: analog of per-command allowlist entries.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — exec tool behavior; relevance: analog of the requested-vs-effective exec policy.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — settings precedence; relevance: direct analog of host-approvals-file vs requested-policy precedence.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permissions; relevance: analog of the `host=auto` sandbox-vs-gateway distinction.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — permission system; relevance: analog of allow/deny rule merging.
- [hermes_code_execution](../hermes_agent/hermes_code_execution.md) — Hermes code execution; relevance: analog of gateway/node exec approval surface.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — Hermes exec isolation; relevance: analog of node-host exec approval policy.
- [oc_cli_agent](oc_cli_agent.md) — (planned, this series) one-shot turn; relevance: the runs these approvals gate.
- [oc_cli_backup](oc_cli_backup.md) — (planned, this series) backup; relevance: the state-dir `exec-approvals.json` is part of the backup payload.
- [oc_cli_browser](oc_cli_browser.md) — (planned, this series) browser; relevance: browser actions via a node host are subject to node exec approvals.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec policy + approvals enforcement; relevance: implements the effective-policy merge.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway-host approvals + node RPC; relevance: backs `--gateway`/`--node` `system.execApprovals.get/set`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent allowlist scope; relevance: backs `--agent` allowlist scoping.

**Snippets**
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: the policy object `approvals set` writes.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: implements the host-approvals-file source of truth.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: backs effective-policy computation/notes.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestrator; relevance: enforces the approved policy at run time.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: backs `--node` host approvals (node + gateway `tools.exec` combine).
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: analog of deny-all preset behavior.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execute; relevance: backs `approvals get` effective-policy probe.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: supervises exec processes governed by approvals.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: gates `system.execApprovals.*` calls behind operator scope.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/SecretRef resolution; relevance: backs SecretRef-managed `tools.exec.*` config.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — openshell exec backend; relevance: the exec backend the approvals govern.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_backup (8t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw backup` archives local OpenClaw state/config.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — OAuth credentials; relevance: model auth profiles (`auth-profiles.json`) are in the backed-up state.
- [Authentication](../../term_dictionary/term_authentication.md) — auth profiles; relevance: `agents/<id>/agent/auth-profiles.json` is covered by the state backup.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — channel/provider credentials; relevance: the resolved `credentials/` dir is a backup source.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: active session transcripts are skipped as volatile (`skippedVolatileCount`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — installed plugins; relevance: plugin source under `extensions/` is included; `node_modules/` is skipped.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway state dir; relevance: the backed-up state directory is the gateway's local state (`~/.openclaw`).
- [Sandbox](../../term_dictionary/term_sandbox.md) — workspace trees; relevance: `--no-include-workspace` controls whether sandbox/workspace trees are archived.

**Docs**
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential/FS controls; relevance: analog of credential/state-store handling in a backup.
- [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — session store layout; relevance: analog of session-transcript state excluded from backup.
- [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — session management; relevance: analog of which session state is durable vs volatile.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed config; relevance: analog of `--only-config` (config-file-only archive).
- [pi_session_file_format](../pi/pi_session_file_format.md) — session file format; relevance: analog of the on-disk session/state files in scope.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth files; relevance: analog of `auth-profiles.json` in the backup payload.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pools; relevance: analog of the `credentials/` dir archived by backup.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — config-file precedence; relevance: analog of "active config file path" backup source.
- [oc_cli_approvals](oc_cli_approvals.md) — (planned, this series) approvals; relevance: state-dir `exec-approvals.json` is part of the backup payload.
- [oc_cli_agents](oc_cli_agents.md) — (planned, this series) agents; relevance: per-agent workspace/state/`auth-profiles.json` are backed up.
- [oc_cli_channels](oc_cli_channels.md) — (planned, this series) channels; relevance: channel/provider credentials dir is a backup source.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — state/config layout; relevance: defines the state-dir tree backup walks.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — credential/auth-profile handling; relevance: governs which credential files are archived.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the `backup` command; relevance: hosts `openclaw backup create/verify`.

**Snippets**
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — state-dir/env resolution; relevance: resolves `$OPENCLAW_STATE_DIR` the backup walks.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — auth-profile portability; relevance: governs `auth-profiles.json` portability across restore.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: identifies the `credentials/` dir to archive.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering; relevance: the auth-profile structure preserved in the archive.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: another credential class in backup scope.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload/plan; relevance: relates to `--only-config` config-file handling.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config apply; relevance: analog of restoring/applying a backed-up config.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/FS policy; relevance: `exec-approvals.json` is part of the state backup.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — session-FS index read; relevance: identifies session-state files (skipped as volatile).
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: backs the "active transcripts skipped" volatile-file rule.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_browser (8t · 12s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw browser` is OpenClaw's browser control surface.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the whole command surface (snapshot/click/type/navigate).
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: CDP profiles point at a local/remote CDP endpoint (`--cdp-url`).
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side request forgery defense; relevance: `open`/`navigate` failures are usually navigation SSRF policy blocks.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the `user` profile drives existing Chrome via Chrome DevTools MCP.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway; relevance: the Gateway proxies browser actions to a node host (`gateway.nodes.browser.*`).
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated profile; relevance: the `openclaw` managed profile uses an isolated user-data-dir.
- [Access Control](../../term_dictionary/term_access_control.md) — upload/path allowlist; relevance: uploads restricted to temp uploads root + managed inbound media; traversal rejected.

**Docs**
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome control via CDP/MCP; relevance: closest existing analog of the whole browser surface.
- [cc_chrome_setup_and_troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — Chrome setup/troubleshooting; relevance: analog of doctor/CDP-readiness/`start` failures.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — network access policy; relevance: analog of navigation SSRF policy on `open`/`navigate`.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS access; relevance: analog of SSRF/network-policy blocking.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: direct analog of profiles/lifecycle setup.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — Hermes browser backends; relevance: direct analog of managed/CDP/existing-session profile backends.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: analog of lifecycle/start/stop/recovery.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox FS/network isolation; relevance: analog of the managed isolated user-data-dir profile + network egress policy.
- [oc_cli_acp_bridge](oc_cli_acp_bridge.md) — (planned, this series) ACP bridge; relevance: both are Gateway-backed CLI surfaces with `--url`/`--token`.
- [oc_cli_channels](oc_cli_channels.md) — (planned, this series) channels; relevance: shares the node-host proxy model.
- [oc_cli_approvals](oc_cli_approvals.md) — (planned, this series) approvals; relevance: remote browser actions on a node host are node-exec-approval governed.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway WS + node-host proxy; relevance: backs `gateway.nodes.browser.mode`/`node` proxy routing.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — navigation SSRF + upload allowlist; relevance: enforces SSRF policy + upload path restrictions.

**Snippets**
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP connection; relevance: analog of `--cdp-url` / CDP-profile attach.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — navigate/click/type; relevance: analog of ref-based `navigate`/`click`/`type` actions.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: analog of `screenshot --full-page`/`--ref`/`--labels`.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM snapshot/refs; relevance: analog of `snapshot`/ref-based element targeting.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session/tabs; relevance: analog of tabs/`suggestedTargetId`/profile session state.
- [snippet_hermes_agent_tools_browser_intercept](../../code_snippets/snippet_hermes_agent_tools_browser_intercept.md) — request interception; relevance: analog of `responsebody`/`requests --filter` debugging.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — browser lifecycle; relevance: analog of `start`/`stop`/`status`/`doctor` lifecycle.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — supervisor recovery; relevance: analog of "not reachable after start" recovery.
- [snippet_hermes_agent_tools_browser_camofox](../../code_snippets/snippet_hermes_agent_tools_browser_camofox.md) — managed browser engine; relevance: analog of the managed `openclaw` isolated-profile browser.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser plugin dispatch; relevance: analog of the bundled browser plugin (`plugins.allow: ["browser"]`).
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: backs the node-host browser proxy command path.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: backs Gateway→node-host browser action proxying.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

### oc_cli_channels (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw channels` manages OpenClaw chat-channel accounts.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — multi-platform account set; relevance: the page spans WhatsApp/Telegram/Discord/Slack/Matrix/Signal/iMessage accounts.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — per-channel transport; relevance: per-channel add flags (token, signal paths, Matrix homeserver) are adapter config.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — runtime channel dispatch; relevance: `status --probe`/`capabilities` hit the runtime channel kernel.
- [Slack](../../term_dictionary/term_slack.md) — Slack channel; relevance: `resolve`/`capabilities` examples and bot/user scope probes use Slack.
- [Webhook](../../term_dictionary/term_webhook.md) — webhook transport; relevance: Google Chat add flags are `--webhook-path`/`--webhook-url`.
- [Authentication](../../term_dictionary/term_authentication.md) — per-channel auth; relevance: `login`/`logout` and add-flags seed per-channel auth.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — SecretRef credentials; relevance: SecretRef-configured channel credentials degrade gracefully when unavailable.
- [Cap Routing](../../term_dictionary/term_cap_routing.md) — channel→agent routing; relevance: interactive add can write account-scoped routing bindings to agents.

**Docs**
- [cc_channel_reply_tool](../claude_code/cc_channel_reply_tool.md) — channel reply tool; relevance: analog of the channel surface accounts feed.
- [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — channel permission relay; relevance: analog of per-channel capability/permission probes.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — channels overview; relevance: analog of the multi-channel account model.
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup; relevance: analog of `channels add`/`login` setup flows.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway architecture; relevance: analog of channel accounts on a gateway.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack messaging setup; relevance: analog of Slack account add/scope probe.
- [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram setup; relevance: analog of Telegram bot-token account add.
- [hermes_webhooks_routing_delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — webhook routing/delivery; relevance: analog of Google Chat webhook account fields + routing.
- [oc_cli_agents](oc_cli_agents.md) — (planned, this series) agents; relevance: the routing bindings the channels wizard writes are managed there.
- [oc_cli_agent](oc_cli_agent.md) — (planned, this series) one-shot turn; relevance: `--reply-channel` delivers replies to these accounts.
- [oc_cli_acp_bridge](oc_cli_acp_bridge.md) — (planned, this series) ACP bridge; relevance: shares the same Gateway whose channel runtime status this reports.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel account management; relevance: implements list/add/remove/status/resolve.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging transports; relevance: implements per-channel transport (Slack socket mode, Telegram, etc.).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — runtime channel status/restart; relevance: backs `status --probe` + listener stop on remove/logout.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — channel credential SecretRef handling; relevance: backs degraded-credential reporting.

**Snippets**
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: backs `channels list`/`--all` installed/configured/enabled tags.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status/probe; relevance: backs `status --probe` (`works`/`probe failed`/`audit ok`).
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — name→ID resolver; relevance: backs `channels resolve --channel slack "#general"`.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: backs `--kind user|group|auto` resolution.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket mode; relevance: backs Slack bot/user scope capability probe.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord intents; relevance: backs `capabilities --channel discord --target` permission flags.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport; relevance: backs `channels add --channel telegram --token`.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: defines the per-channel add-flag surface.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: the runtime dispatch behind status/probe.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: backs listener stop/restart on `remove`/`logout`.
- [snippet_openclaw_gateway_channels_runtime_snapshot](../../code_snippets/snippet_openclaw_gateway_channels_runtime_snapshot.md) — channel runtime snapshot; relevance: backs config-only fallback when the gateway is unreachable.

**Entry point:** [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — (planned, W1) OpenClaw docs hub; relevance: primary anti-island inbound link.

> Confirmed MISSING and therefore NOT cited: `term_codex`, `term_secretref`, `term_gateway`, `term_zed`,
> `term_chrome_mcp` — substituted by `term_autonomous_coding_agents`/`term_claude_code`,
> `term_secrets_manager`, `term_messaging_gateway`, `term_acp_agent_client_protocol`, `term_mcp` respectively.
> `term_pi_agent`/`term_function_calling`/`term_fallback_provider`/`term_provider_routing` DO exist; used only
> where relevance holds (`term_function_calling`/`term_fallback_provider` in note 3). The browser-snippet gap
> flagged at draft is RESOLVED: the Hermes browser snippet corpus (`snippet_hermes_agent_tools_browser_*`,

## Undigested Terms Plan

Per master: OpenClaw CLI vocabulary is documented as `oc_*` doc notes (these command pages), NOT promoted to
new `term_dictionary` entries. The only term interaction is LINKING existing terms (verified above). **Expected
0 new `term_dictionary` captures.** Augment re-runs the Step 2d new-term scan.

| Term (appears in source) | Disposition |
|---|---|
| ACP / Agent Client Protocol | Link existing `term_acp_agent_client_protocol`. |
| ACP bridge / `openclaw acp` | Documented in `oc_cli_acp_bridge` (this series); not a term note. |
| ACP harness / `acpx` / `/acp spawn` | Link-out to `tools/acp-agents*` (to01); not a term note. |
| MCP / `openclaw mcp serve` | Link existing `term_mcp`. |
| JSON-RPC / ACP frames | Link existing `term_json_rpc`. |
| Gateway / WebSocket transport | Link existing `term_messaging_gateway` + `term_websocket`. |
| Session key / session mapping / lineage | Link existing `term_session_persistence` (+ `term_subagent` for lineage). |
| Isolated agents / routing bindings | Documented in `oc_cli_agents`; link `term_multi_agent`, `term_cap_routing`, `term_channel_adapter`. |
| Exec approvals / exec-policy / allowlist / YOLO | Documented in `oc_cli_approvals`; link `term_access_control`, `term_sandbox`; concept link-out `tools/exec-approvals`. |
| Browser profiles / CDP / Chrome MCP / SSRF | Documented in `oc_cli_browser`; link `term_browser_automation`, `term_cdp`, `term_mcp`, `term_ssrf_guard`. |
| Channels / accounts / capabilities probe | Documented in `oc_cli_channels`; link `term_omnichannel`, `term_channel_adapter`, `term_channel_kernel`. |
| SecretRef / `secretref-env` / credentials | Link existing `term_secrets_manager` (no `term_secretref` note exists — do NOT create; SecretRef is config syntax, not a vault-reusable cross-cutting term — covered by `term_secrets_manager`). |
| backup archive / manifest.json | Documented in `oc_cli_backup`; not a term note. |
| deliveryStatus / delivery outcomes | Documented in `oc_cli_agent` (JSON delivery status); not a term note. |

**New-term candidates: 0.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an
existing note was found — every concept either has a doc-page home (`oc_*`) or an existing `term_dictionary`
note to link. (SecretRef explicitly NOT promoted: config-syntax, subsumed by `term_secrets_manager`.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes. Inherited from master: if augment's
Step 2d scan surfaces a genuinely reusable cross-cutting term with no doc-page home AND no existing note, it
`acronym_glossary_*.md` (here: `acronym_glossary_agentic_ai.md` / the agentic-AI glossary) — not expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + body H2s `## Overview` / `## Related Notes` + `**Source**`/`**Last Updated**`/`**Status**` footer; density caps ≤400L/≤2500w/≤6 code; one BB) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to the source page) | diff each `oc_cli_*.md` vs `inbox/openclaw_docs/cli/<page>.md` |
| G3 | Density + Coverage (every H2/H3 mapped; no over-compression; caps respected) | Section Coverage Map above + density re-assessment |
| G4 | Cross-Reference (≥6 relevance-selected terms + repos/siblings/other-vault per note, each with relevance statement) | review `## Related Notes` per note |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | `/tessellum-fix-ghost-references` + `note_links` query |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` | inbound-link map (below) — satisfied via `entry_openclaw_docs.md` |
| G8 | In-degree ≥1 (anti-island) per new note | `notes.in_degree` after reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_acp_bridge oc_cli_acp_compatibility oc_cli_agent oc_cli_agents oc_cli_approvals oc_cli_backup oc_cli_browser oc_cli_channels"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + broken-link (LINK-003)
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url:' "$f" || echo "$n MISSING source_url"; }
  # density caps (body only, excludes frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G7/G8 sibling/inbound presence (≥1 oc_ sibling link expected)
  grep -qE "\($SIBLING_PREFIX" "$f" || echo "$n: no $SIBLING_PREFIX sibling link found"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference sweep + G8 in-degree after incremental reindex
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  echo "$n in_degree=${indeg:-NULL}"; { [ "${indeg:-0}" -lt 1 ] && echo "G8 FAIL (island): $n"; } 2>/dev/null
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source words | Within caps (≤400L/≤2500w/≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_cli_acp_bridge | procedure | 650 | 2,132 (shared w/ #2) | ✅ (bash blocks pruned to ≤6 representative) |
| 2 | oc_cli_acp_compatibility | model | 550 | 2,132 (shared w/ #1) | ✅ (1 JSON ledger block + 2 matrix tables) |
| 3 | oc_cli_agent | procedure | 500 | 1,062 | ✅ |
| 4 | oc_cli_agents | procedure | 600 | 960 | ✅ |
| 5 | oc_cli_approvals | procedure | 600 | 860 | ✅ |
| 6 | oc_cli_backup | procedure | 450 | 737 | ✅ |
| 7 | oc_cli_browser | procedure | 700 | 1,721 | ✅ (15 source fences → ≤6 grouped command blocks) |
| 8 | oc_cli_channels | procedure | 600 | 1,195 | ✅ |

No note approaches the caps. The only code-heavy pages are `acp` (12 fences, split mitigates) and `browser`
(15 fences); both note(s) reproduce only representative command groups to stay ≤6 code blocks.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `0_entry_points/entry_openclaw_docs.md` (CREATED as a master W1 pre-step before the
first sub-plan executes) under a "CLI" cluster. Each new `oc_cli_*` note receives its entry-point back-link at
finalization — this is the primary G7/G8 inbound-link source. Master W2/W3 (parent-hub `entry_gen_ai_dev`,

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all listed targets verified present
2026-06-20):

- `entry_openclaw_docs.md` (planned, W1) → **all 8 notes** (primary anti-island source).
- `repo_openclaw_cli_wizard.md` → notes 1, 3, 4, 6 (the CLI dispatch hosting these commands).
- `repo_openclaw_agents.md` → notes 1, 2, 3, 4 (ACP runtime + agent CRUD/run).
- `repo_openclaw_gateway.md` → notes 1, 2, 3, 7 (WS endpoint / chat handlers / browser node proxy).
- `repo_openclaw_channels.md` → notes 4, 8 (bindings + channel accounts).
- `repo_openclaw_security.md` → notes 5, 6, 7, 8 (exec approvals, credential backup, SSRF, channel creds).
- `repo_openclaw_apps.md` → note 7 (browser control surface).
- `term_acp_agent_client_protocol.md` → notes 1, 2.
- `term_browser_automation.md` → note 7; `term_cdp.md` → note 7.
- `term_multi_agent.md` → note 4; `term_omnichannel.md` → notes 4, 8.
- `term_openclaw.md` → all 8 (reciprocal, where relevant).

## Pacing Rules (inherited from master)

One execution phase (8 notes ≤ ~30 fan-out cap). Re-read each source page; reproduce command/JSON blocks
verbatim. One BB per note. Run the full 9-GATE before commit; incremental reindex; verify `note_links` +
0 broken links + in-degree ≥1; `git pull --rebase --autostash origin main` first; commit + push per wave; no
Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (plan is `ready`) |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of sub-plan cl01 (CLI: acp, agent, agents, approvals, backup, browser, channels).
Re-read all 7 source mirrors under `inbox/openclaw_docs/cli/` (acp 2,132w · agent 1,062w · agents 960w ·
approvals 860w · backup 737w · browser 1,721w · channels 1,195w = 8,667w measured, matching the Source table).
Built and LOCKED the per-note Related Notes mapping at the RAISED floors (≥8 `term_dictionary` terms · ≥10
`code_snippets` · ≥10 docs under `resources/documentation/` per note), relevance-selected against the re-read


| Note | Terms | Snippets | Docs | Repos | Floors met |
|---|---:|---:|---:|---:|---|
| oc_cli_acp_bridge | 9 | 12 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_acp_compatibility | 8 | 11 | 10 (8 existing + 2 planned sib) | 3 | ✅ |
| oc_cli_agent | 8 | 11 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_agents | 9 | 11 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_approvals | 8 | 11 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_backup | 8 | 10 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_browser | 8 | 12 | 11 (8 existing + 3 planned sib) | 3 | ✅ |
| oc_cli_channels | 9 | 11 | 11 (8 existing + 3 planned sib) | 4 | ✅ |

term/snippet/repo/doc targets resolve; planned `oc_cli_*` siblings + planned `entry_openclaw_docs` are the only
non-resolving links, correctly marked "(planned)"). Relative paths verified from
`resources/documentation/openclaw/oc_X.md` (`../../term_dictionary/`, `../../code_snippets/`,
`../../../areas/code_repos/`, `../<folder>/`, `../../../0_entry_points/`).

**Key resolution — browser-snippet gap (flagged at draft) is CLOSED:** the draft noted no
`snippet_openclaw_*browser*` exists. The Hermes browser snippet corpus
(`snippet_hermes_agent_tools_browser_*` ×9 + `snippet_hermes_agent_plugins_browser_dispatch`) supplies note 7's
full snippet floor (12 snippets), supplemented by `snippet_openclaw_gateway_node_command_policy` /
`snippet_openclaw_gateway_nodes_command_apns_invoke` for the node-host proxy path. `repo_openclaw_apps`

**DB substitutions confirmed (draft notes carried forward):** MISSING and NOT cited — `term_codex`,
`term_secretref`, `term_gateway`, `term_zed`, `term_chrome_mcp`. Substitutes:
`term_autonomous_coding_agents`/`term_claude_code`, `term_secrets_manager`, `term_messaging_gateway`,
`term_acp_agent_client_protocol`, `term_mcp`. `term_pi_agent`/`term_function_calling`/`term_fallback_provider`/
`term_provider_routing` exist; cited only where relevance holds (`term_function_calling` + `term_fallback_provider`
in note 3 `oc_cli_agent`; `term_provider_routing` not cited — `term_cap_routing` is the more specific routing-binding term).

**New-term candidates: 0.** Step 2d re-read scan surfaced no genuinely cross-cutting, vault-reusable term
lacking BOTH a doc-page home AND an existing note. Every concept in the 7 pages either has an `oc_*` doc-page
home (this series) or an existing `term_dictionary` note to link (verified). SecretRef remains explicitly NOT
promoted (config-syntax subsumed by `term_secrets_manager`). The Undigested Terms Plan (0 captures, link-only)
is unchanged and re-validated. **Best-fit glossary (if a term ever surfaced): `acronym_glossary_agentic_ai.md`**
(agentic/LLM glossary) per master W5 — not exercised here.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | LOCKED mapping present per note; programmatic counts ≥8t/≥10s/≥10d for all 8 notes; every link carries `relevance:`; 0 bare links. |
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present; G5 ghost-detect (`/tessellum-fix-ghost-references` + `note_links`) and G6 broken-link-fix (`/tessellum-fix-broken-links`) both present; single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "Entry Point Decision" + "Inlinks" specify `entry_openclaw_docs.md` (CREATE at master W1 pre-step) → all 8 notes as the primary G7/G8 inbound source; each note's mapping carries the entry-point back-link. |
| CP4 | Plan size (≤30 notes or split) | **PASS** | 8 planned notes, well under the 30 cap; single execution phase. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Format Definition inherited verbatim from master (derived from `claude_code/` `cc_*` + `pi/` `pi_*` corpora: `## Overview`/`## Related Notes`/`**Source**` footer, fixed YAML field order, forbidden-field list). |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: max note ~700w (acp_bridge/browser) vs caps ≤2,500w/≤400L/≤6 code; `acp.md` (2,132w, mixed BB) already split into procedure + model notes; no borderline note unaddressed. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 mirrors re-read 2026-06-21; measured words match the Source table (total 8,667w); `wc -w` basis recorded. |
| CP8 | Undigested terms + authoring reqs | **PASS** | Undigested Terms Plan present (link-only, 0 captures); Term-Note Authoring Requirements N/A documented (0 new terms) with master-inherited fallback to `/tessellum-capture-term-note` + `acronym_glossary_agentic_ai.md` if a term ever surfaces. |
| CP8f | Term-slug specificity + all-notes dedup/collision audit | **PASS** | 0 new term slugs (nothing to rename). Doc-note collision audit: each planned `oc_cli_*` is a command-reference page with no existing same-concept `term_*`/doc note (the OpenClaw CLI surface is undocumented on the docs side); existing `term_*`/`repo_openclaw*`/`oc_*` are LINKED not duplicated. |
| CP9 | Discoverability / inlinks (G8, no islands) | **PASS** | Inlinks table maps existing repos/terms + `entry_openclaw_docs` → all 8 notes (≥1 outside-folder inbound each); G8 in-degree ≥1 check present in the validation script; inlinks are a gated execution phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
