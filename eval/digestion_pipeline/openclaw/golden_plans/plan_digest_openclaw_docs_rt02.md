---
title: Sub-Plan rt02 — OpenClaw Docs: Top-level (date-time, gateway, help, install, logging, network, nodes)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["date-time", "gateway", "help", "install", "logging", "network", "nodes"]
---

# Sub-Plan rt02: Top-level

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, Overview →
> mirrored body → Related Notes → References → bold footer), dedup-before-create (term_dictionary + documentation/ +
> repo_openclaw*), 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 top-level (root-slug) OpenClaw doc pages that have no folder prefix: `date-time`, `gateway`, `help`,
`install`, `logging`, `network`, `nodes`. These are the operator-facing **hubs and runbooks** that sit at the
root of the docs tree and link out to the deeper `/gateway/*`, `/cli/*`, `/install/*`, `/channels/*`, and
`/nodes/*` sections. They define the day-1/day-2 operational vocabulary (gateway lifecycle, install paths, log
surfaces, node pairing/capabilities, network/security posture, time handling) the rest of the corpus references.
**Priority P1 (Phase A)** — conceptual/operational core. The code-side counterparts (`repo_openclaw_gateway`,
`repo_openclaw_agents`, `repo_openclaw_security`, etc.) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **7,758 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| date-time | /date-time | 503 | 8 | 5 | 1 | procedure |
| gateway | /gateway | 1,563 | 15 | 16 | 3 | procedure + concept (split: runbook vs runtime/protocol) |
| help | /help | 213 | 0 | 4 | 0 | concept (navigation hub) |
| install | /install | 819 | 6 | 8 | 6 | procedure |
| logging | /logging | 1,715 | 8 | 9 | 10 | procedure (split: surfaces vs configuration) |
| network | /network | 313 | 0 | 6 | 0 | concept (navigation/architecture hub) |
| nodes | /nodes | 2,632 | 25 | 18 | 6 | procedure + concept (split ×3: pairing/host vs capabilities vs command-policy) |

> Code counts are `grep -c '^```' / 2` (fence pairs). `gateway.md` and `nodes.md` also contain Mintlify JSX
> components (`<CardGroup>`, `<Steps>`, `<Tabs>`, `<Note>`, `<Warning>`) that are flattened to prose/links in the
> digest, not reproduced as code.

## Content Strategy

- **Prioritize**: the gateway runbook (startup/health/supervision — every operation depends on a running
  gateway), the install paths (entry to the whole product), node pairing + command-policy (the security-sensitive
  capability surface), and the log surfaces + configuration (the primary troubleshooting tool). These are the
  load-bearing operational concepts.
- **Split** (per word-cap >2,500 OR mixed-BB rules): `nodes.md` (2,632w, 25 fences, procedure+concept) → 3 notes;
  `gateway.md` (1,563w, mixed runbook-procedure + runtime/protocol-concept + failure reference) → 2 notes;
  `logging.md` (1,715w, 8 fences, surfaces-procedure + configuration/diagnostics-procedure, two task clusters) →
  2 notes. The three hubs/leaf pages (`date-time`, `help`, `install`, `network`) stay 1 note each.
- **Link-out / do not redefine**: CLI subcommand detail (`cli/node`, `cli/devices`, `cli/logs`, `cli/gateway`) →
  `cl0*` sub-plans; gateway config/secrets/auth/protocol/discovery/remote/opentelemetry leaf pages → `gw0*`;
  channel pairing → `ch0*`; per-platform node runbooks (iOS/Android/mac) → `pf0*`; concepts (architecture,
  system-prompt, timezone, messages) → `co0*`; diagnostics flags → `dg01`; install leaf pages (docker, k8s,
  installer, updating, migrating, node) → `in0*` and `rt03` (vps). Existing terms
  (`term_openclaw`/`term_mcp`/`term_websocket`/`term_json_rpc`/`term_oauth_token`/`term_cron`/`term_sandbox`/…)
  are LINKED, never inlined. Provider/platform names mentioned in passing are not promoted to term notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_date_time.md` | procedure | date-time.md (all H2/H3) | 500 | How OpenClaw handles dates/times: host-local envelope timestamps by default, user-timezone in the system prompt (zone-only for cache stability), `envelopeTimezone`/`envelopeTimestamp`/`envelopeElapsed`/`userTimezone`/`timeFormat` config, auto time-format detection, and raw-provider + normalized (`timestampMs`/`timestampUtc`) fields in tool payloads. |
| 2 | `oc_gateway_runbook.md` | procedure | gateway.md: 5-minute local startup, Operator command set, Multiple gateways, Remote access, Supervision and service lifecycle, Dev profile quick path, Operational checks, Common failure signatures | 700 | Day-1/day-2 Gateway runbook: start/verify/probe, operator commands, running multiple isolated gateways, remote access (Tailscale/SSH tunnel), supervised service install per OS (launchd/systemd/Scheduled Task), liveness/readiness/gap-recovery checks, and common failure signatures. |
| 3 | `oc_gateway_runtime_protocol.md` | concept | gateway.md: Runtime model, OpenAI-compatible endpoints, Port and bind precedence, Hot reload modes, Protocol quick reference, Safety guarantees | 650 | The Gateway runtime model: one always-on multiplexed process for WS control/RPC, OpenAI-compatible HTTP endpoints (`/v1/models|embeddings|chat/completions|responses`, `/tools/invoke`), port/bind precedence, hot-reload modes, the operator-view protocol handshake (`connect` → `hello-ok` → `req/res` + events, two-stage agent runs), and safety guarantees. |
| 4 | `oc_help.md` | concept | help.md (all H2) | 350 | The Help hub: a symptom-first "get unstuck" index pointing to troubleshooting, debugging, install sanity, gateway troubleshooting, doctor, the FAQ set (general / first-run / models), diagnostics (env vars, flags, node crash), testing pages, and community/meta docs. |
| 5 | `oc_install.md` | procedure | install.md (all H2/H3) | 650 | Installing OpenClaw beyond the quickstart: system requirements (Node 24/22.19+), the recommended installer script (macOS/Linux/WSL2 + Windows PowerShell, `--no-onboard`), alternatives (local-prefix `install-cli.sh`, npm/pnpm/bun, from source, GitHub main, containers/package managers), install verification, hosting/deployment targets, update/migrate/uninstall pointers, and the `openclaw not found` PATH fix. |
| 6 | `oc_logging_surfaces.md` | procedure | logging.md: Where logs live, How to read logs (CLI live tail, Control UI, channel-only), Log formats (File JSONL, Console, Gateway WebSocket), Troubleshooting tips | 650 | OpenClaw's log surfaces: rolling JSONL file logs under `/tmp/openclaw/`, reading them via `openclaw logs --follow` (output modes, JSON `type` tags, fallback behavior), the Control UI Logs tab, channel-only logs, the file-JSONL/console/Gateway-WebSocket formats, and quick troubleshooting tips. |
| 7 | `oc_logging_configuration.md` | procedure | logging.md: Configuring logging, Log levels, Targeted model transport diagnostics, Trace correlation, Model call size and timing, Console styles, Redaction, Diagnostics and OpenTelemetry | 700 | Configuring logging: `logging.*` config (level/consoleLevel/file/consoleStyle), `OPENCLAW_LOG_LEVEL`/`--log-level` precedence, targeted `OPENCLAW_DEBUG_*` model-transport flags, trace correlation (traceId/spanId, OTEL/traceparent), bounded model-call size/timing fields, console styles, secret redaction (`redactSensitive`/`redactPatterns`, safety-boundary always-on), and the diagnostics/OpenTelemetry relationship. |
| 8 | `oc_nodes_pairing_host.md` | procedure | nodes.md: (intro), Pairing + status, Remote node host (system.run) incl. What runs where, Start a node host (foreground/service), Remote gateway via SSH tunnel, Pair + name, Allowlist the commands, Point exec at the node, Headless node host, Mac node mode | 700 | Pairing and running OpenClaw nodes: device-pairing handshake + approval scopes, the remote node host (`openclaw node run/install`) for off-gateway `system.run`, SSH-tunnel connection to a loopback-bound gateway, naming, per-node exec allowlists, pointing `tools.exec` at a node, the cross-platform headless node host, and Mac node mode. |
| 9 | `oc_nodes_capabilities.md` | procedure | nodes.md: Invoking commands, Screenshots (canvas snapshots) + Canvas controls + A2UI, Photos + videos (camera), Screen recordings, Location, SMS (Android), Android device + personal data commands, System commands, Exec node binding, Permissions map | 700 | The node capability/command surface and CLI helpers: `nodes invoke`, canvas snapshot/present/navigate/eval + A2UI push, camera photos/clips, screen recording, location, Android SMS, Android device/notifications/contacts/calendar/photos commands, node-host system commands (`system.run`/`system.which`/`system.notify`), exec node binding, and the node permissions map. |
| 10 | `oc_nodes_command_policy.md` | concept | nodes.md: Command policy, Config (`openclaw.json`) `gateway.nodes`/`tools.exec` | 550 | The node command-policy/permission model: the two-gate check (node-declared `connect.commands` AND gateway platform policy), default-allowed vs opt-in dangerous commands (`gateway.nodes.allowCommands`/`denyCommands`, deny-wins), plugin node-invoke policy, CIDR auto-approve pairing, and the `gateway.nodes`/`tools.exec` config schema (host/security/node, per-agent override). |
| 11 | `oc_network.md` | concept | network.md (all H2) | 350 | The OpenClaw network architecture/security hub: the loopback-first Gateway core model (single WS control plane, one gateway per host, canvas on the same port, auth required beyond loopback), pairing + identity (local-trust auto-approve vs explicit tailnet/LAN approval), discovery + transports, nodes as peripherals, and the canonical list of networking/security/discovery docs. |

## Section Coverage Map

```
date-time.md
├── Message envelopes (local by default) + Examples ─────────── → note 1 (oc_date_time)
├── System prompt: current date and time ───────────────────── → note 1
├── System event lines + Configure user timezone + format ──── → note 1
├── Time format detection (auto) ───────────────────────────── → note 1
├── Tool payloads + connectors (raw + normalized fields) ───── → note 1
└── Related docs (System Prompt/Timezones/Messages) ────────── → note 1 References (link-out to co0*)
gateway.md
├── (CardGroup: troubleshooting/configuration/secrets/secrets-plan) → note 2 References (link-out gw0*)
├── 5-minute local startup ─────────────────────────────────── → note 2 (oc_gateway_runbook)
├── Runtime model ──────────────────────────────────────────── → note 3 (oc_gateway_runtime_protocol)
├── OpenAI-compatible endpoints ────────────────────────────── → note 3
├── Port and bind precedence ───────────────────────────────── → note 3
├── Hot reload modes ───────────────────────────────────────── → note 3
├── Operator command set ───────────────────────────────────── → note 2
├── Multiple gateways (same host) ──────────────────────────── → note 2
├── Remote access ──────────────────────────────────────────── → note 2
├── Supervision and service lifecycle (launchd/systemd/Win) ── → note 2
├── Dev profile quick path ─────────────────────────────────── → note 2
├── Protocol quick reference (operator view) ───────────────── → note 3
├── Operational checks (Liveness/Readiness/Gap recovery) ───── → note 2
├── Common failure signatures ──────────────────────────────── → note 2
├── Safety guarantees ──────────────────────────────────────── → note 3
└── Related ────────────────────────────────────────────────── → notes 2/3 References (link-out gw0*)
help.md
├── (intro: get-unstuck path) ──────────────────────────────── → note 4 (oc_help) Overview
├── FAQ ────────────────────────────────────────────────────── → note 4
├── Diagnostics ────────────────────────────────────────────── → note 4
├── Testing ────────────────────────────────────────────────── → note 4
└── Community and meta ─────────────────────────────────────── → note 4
install.md
├── System requirements ────────────────────────────────────── → note 5 (oc_install)
├── Recommended: installer script ──────────────────────────── → note 5
├── Alternative install methods (prefix/npm-pnpm-bun/source/git/containers) → note 5 (+ H3s)
├── Verify the install ─────────────────────────────────────── → note 5
├── Hosting and deployment (VPS/Docker VM/K8s/Fly/…) ───────── → note 5 (link-out in0*/rt03 vps)
├── Update, migrate, or uninstall ──────────────────────────── → note 5 (link-out in0*)
└── Troubleshooting: `openclaw` not found ──────────────────── → note 5
logging.md
├── Where logs live ────────────────────────────────────────── → note 6 (oc_logging_surfaces)
├── How to read logs (CLI tail / Control UI / channel-only) ── → note 6
├── Log formats (File JSONL / Console / Gateway WebSocket) ──── → note 6
├── Configuring logging ────────────────────────────────────── → note 7 (oc_logging_configuration)
├── Log levels ─────────────────────────────────────────────── → note 7
├── Targeted model transport diagnostics ───────────────────── → note 7
├── Trace correlation ──────────────────────────────────────── → note 7
├── Model call size and timing ─────────────────────────────── → note 7
├── Console styles ─────────────────────────────────────────── → note 7
├── Redaction ──────────────────────────────────────────────── → note 7
├── Diagnostics and OpenTelemetry ──────────────────────────── → note 7 (link-out gateway/opentelemetry → gw0*, dg01)
├── Troubleshooting tips ───────────────────────────────────── → note 6
└── Related ────────────────────────────────────────────────── → notes 6/7 References
network.md
├── (intro hub) ────────────────────────────────────────────── → note 11 (oc_network) Overview
├── Core model ─────────────────────────────────────────────── → note 11
├── Pairing + identity ─────────────────────────────────────── → note 11
├── Discovery + transports ─────────────────────────────────── → note 11
├── Nodes + transports ─────────────────────────────────────── → note 11
├── Security ───────────────────────────────────────────────── → note 11
└── Related ────────────────────────────────────────────────── → note 11 References
nodes.md
├── (intro: what a node is / node mode / peripherals) ──────── → note 8 (oc_nodes_pairing_host) Overview
├── Pairing + status ───────────────────────────────────────── → note 8
├── Remote node host (system.run) + What runs where ────────── → note 8
├── Start a node host (foreground) ─────────────────────────── → note 8
├── Remote gateway via SSH tunnel (loopback bind) ──────────── → note 8
├── Start a node host (service) ────────────────────────────── → note 8
├── Pair + name ────────────────────────────────────────────── → note 8
├── Allowlist the commands ─────────────────────────────────── → note 8
├── Point exec at the node ─────────────────────────────────── → note 8
├── Invoking commands ──────────────────────────────────────── → note 9 (oc_nodes_capabilities)
├── Command policy ─────────────────────────────────────────── → note 10 (oc_nodes_command_policy)
├── Config (`openclaw.json`) gateway.nodes / tools.exec ────── → note 10
├── Screenshots (canvas snapshots) + Canvas controls + A2UI ── → note 9
├── Photos + videos (node camera) ──────────────────────────── → note 9
├── Screen recordings (nodes) ──────────────────────────────── → note 9
├── Location (nodes) ───────────────────────────────────────── → note 9
├── SMS (Android nodes) ────────────────────────────────────── → note 9
├── Android device + personal data commands ────────────────── → note 9
├── System commands (node host / mac node) ─────────────────── → note 9
├── Exec node binding ──────────────────────────────────────── → note 9
├── Permissions map ────────────────────────────────────────── → note 9
├── Headless node host (cross-platform) ────────────────────── → note 8
└── Mac node mode ──────────────────────────────────────────── → note 8
```
No orphaned sections. CLI subcommand pages, gateway/install/channel/platform/concept leaf pages, and
diagnostics flags are link-outs to their owning sub-plans (cl0*/gw0*/in0*/ch0*/pf0*/co0*/dg01/rt03), not
duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| nodes.md (2,632w, 25 fences, 18 H2/6 H3, mixed BB) | notes 8 + 9 + 10 | Exceeds 2,500w word cap AND mixes three clusters: a pairing/host-setup **procedure** (note 8), a capability/CLI-command **procedure** (note 9, the bulk of the code fences), and a command-policy/permission **concept** with config schema (note 10). 25 fences cannot fit ≤6/note without a 3-way split; each split note stays ≤6 code blocks and ≤700w. |
| gateway.md (1,563w, 15 fences, mixed BB) | notes 2 + 3 | Mixed-BB: a hands-on operations **runbook procedure** (startup/commands/supervision/remote/checks/failures — note 2) vs a **concept/model** of the runtime (always-on process, OpenAI endpoints, port/bind precedence, hot-reload modes, protocol handshake, safety guarantees — note 3). One BB per note; also keeps each ≤6 code blocks (runbook ~9 fences, runtime ~3 → balanced to ≤6 by reproducing only load-bearing snippets). |
| logging.md (1,715w, 8 fences, 9 H2/10 H3) | notes 6 + 7 | Two distinct task clusters: **finding/reading logs** (where they live, CLI tail, Control UI, formats, troubleshooting — note 6) vs **configuring logging** (levels, debug flags, trace correlation, redaction, diagnostics/OTel — note 7). Splitting keeps each focused, single-BB procedure, ≤700w, ≤6 code blocks. |

The four hub/leaf pages stay 1 note each: `date-time` (503w, single coherent procedure), `help` (213w,
navigation hub), `install` (819w, single install procedure), `network` (313w, navigation/architecture hub).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (7,758 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×7 (notes 1, 2, 5, 6, 7, 8, 9) · concept ×4 (notes 3, 4, 10, 11).
- Est. digest words: ~6,950 (avg ~630/note); each note ≤2,500w / ≤400 lines / ≤6 code blocks (one BB each).
- Source code fences (62 total across the 7 pages) distribute across the procedure notes; code-heavy `nodes.md`
  (25) and `gateway.md` (15) split so each digest note reproduces ≤6 load-bearing snippets verbatim.
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** see `## Per-Note Related Notes Mapping (LOCKED)`. Each
  of the 11 notes carries **≥8 relevance-selected `term_dictionary` term notes · ≥10 existing `code_snippets` ·
  11 notes; per-link relevance statements present for the executor to copy verbatim.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21,
docs are **sibling `oc_*` notes (planned, this series)** created by this same sub-plan. Relative paths from
`resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/`; sibling oc_ → `oc_Y.md`; other
doc → `../<folder>/`; repo → `../../../areas/code_repos/`; snippet → `../../code_snippets/`.

### oc_date_time (8t · 10s · 11d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/agent product; relevance: this page documents OpenClaw's own date/time envelope + system-prompt behavior.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: timestamps and timezone are injected into the model's system prompt and message envelopes.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the default agent model that consumes the "Current Date & Time" prompt section.
- [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — reuse of a cached prompt prefix; relevance: the page injects time-zone-ONLY (no clock) specifically to keep the prompt prefix cache-stable.
- [term_context_window](../../term_dictionary/term_context_window.md) — the model's input budget; relevance: envelope timestamp/elapsed prefixes consume context, hence the on/off toggles documented here.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: channel tools return raw + normalized (`timestampMs`/`timestampUtc`) time fields to the agent via tool calls.
- [term_prompt_engineering](../../term_dictionary/term_prompt_engineering.md) — structuring model input; relevance: the dedicated "Current Date & Time" system-prompt section is a prompt-engineering convention for time grounding.
- [term_websocket](../../term_dictionary/term_websocket.md) — the gateway's persistent transport; relevance: system event lines and `session_status` (which carries the current time) flow over the WS control plane.

**Docs** (11; ≥5 existing)
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — Claude Code env/locale config; relevance: analog of OpenClaw's host-locale + timezone configuration for an agent runtime.
- [cc_cli_system_prompt_flags](../claude_code/cc_cli_system_prompt_flags.md) — system-prompt control flags; relevance: analog mechanism for injecting context (incl. time) into an agent system prompt.
- [pi_overview](../pi/pi_overview.md) — pi coding-agent overview; relevance: sibling self-hosted coding-agent whose session model also surfaces current-time/status to the model.
- [pi_sessions](../pi/pi_sessions.md) — pi session model; relevance: analog of how a coding-agent session tracks/surfaces timestamps for messages.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — hermes config precedence; relevance: analog of the `agents.defaults.*` config-override precedence used here for `envelopeTimezone`/`timeFormat`.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) gateway runtime + system prompt; relevance: owns the runtime that assembles the time-bearing system prompt.
- [oc_logging_surfaces](oc_logging_surfaces.md) — (planned, this series) log surfaces; relevance: log lines carry the same host-local-default timestamps described here.
- [oc_logging_configuration](oc_logging_configuration.md) — (planned, this series) `--local-time` log rendering; relevance: shares the local-vs-UTC timestamp rendering choice.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) `session_status`/status card; relevance: the status card timestamp line is the agent's source of "current time".
- [oc_help](oc_help.md) — (planned, this series) help hub; relevance: time-format debugging is a "get unstuck" path linked from help.
- [oc_network](oc_network.md) — (planned, this series) network hub; relevance: cross-host timezone differences matter for remote/tailnet gateway envelopes.

**Repos** (2)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/system-prompt assembly; relevance: implements envelope timestamping + the system-prompt time section.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella repo; relevance: top-level home of the date/time config schema.

**Snippets** (10)
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — cache-stable prompt section assembly; relevance: implements the zone-only "Current Date & Time" section kept out of the cache-volatile area.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — context injection into the system prompt; relevance: how the timezone line is injected.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — Anthropic prompt-prefix handling; relevance: the cache-prefix boundary that the zone-only design protects.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript/envelope assembly; relevance: builds the `[Provider … timestamp]` message envelope.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — timed chat heartbeat/delta; relevance: elapsed-time (`+2m`) suffix logic operates on these timestamps.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance/timestamps; relevance: stamps inbound messages with second-precision time.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — latency/cache-status accounting; relevance: cache stability impact of prompt-prefix time fields.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status/`session_status`; relevance: status card carrying the current-time line the agent reads.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model/locale catalog; relevance: auto time-format detection follows OS/locale prefs resolved here.

### oc_gateway_runbook (9t · 11s · 11d)

**Terms** (9)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: this is OpenClaw's own gateway day-1/day-2 runbook.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS control/RPC plane; relevance: liveness check opens a WS and sends `connect`.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — req/res RPC over WS; relevance: `gateway status --require-rpc` proves read-scope RPC, not just reachability.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer token auth; relevance: shared-secret `gateway.auth.token`/`OPENCLAW_GATEWAY_TOKEN` still required over SSH tunnel.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probing; relevance: `gateway status`/`health`/`channels status --probe` are the readiness ladder.
- [term_vpn](../../term_dictionary/term_vpn.md) — virtual private network; relevance: preferred remote-access path is Tailscale/VPN over SSH tunnel.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: auth required by default; `unauthorized`/`refusing to bind … without auth` are documented failure signatures.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: non-loopback bind uses `gateway.auth.mode: "trusted-proxy"`.
- [term_runbook](../../term_dictionary/term_runbook.md) — operational procedure doc; relevance: this note IS a service runbook (start/verify/probe/recover).

**Docs** (11; ≥5 existing)
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — hermes gateway ops; relevance: direct analog runbook for a coding-agent gateway service.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — hermes gateway internals; relevance: analog of the always-on multiplexed gateway process model.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code proxy/gateway config; relevance: analog of port/bind/proxy operator configuration.
- [pi_cli_reference](../pi/pi_cli_reference.md) — pi CLI reference; relevance: analog operator command set (`status`/`restart`/`stop`).
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — hermes remote/dashboard auth; relevance: analog of remote access + auth-over-tunnel posture.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) runtime/protocol; relevance: the runtime model this runbook operates.
- [oc_network](oc_network.md) — (planned, this series) network/bind hub; relevance: loopback-first + remote access posture the runbook follows.
- [oc_logging_surfaces](oc_logging_surfaces.md) — (planned, this series) log surfaces; relevance: `openclaw logs --follow` is part of the verify/troubleshoot ladder.
- [oc_install](oc_install.md) — (planned, this series) install; relevance: install verification (`gateway status`) hands off to this runbook.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) node host; relevance: node hosts attach to the gateway this runbook drives.
- [oc_help](oc_help.md) — (planned, this series) help hub; relevance: gateway troubleshooting/doctor are linked from help.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service repo; relevance: implements the service/lifecycle/health this runbook drives.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella + CLI; relevance: home of `openclaw gateway …` operator commands.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/bind enforcement; relevance: enforces the "refuse non-loopback bind without auth" guarantee.

**Snippets** (11)
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener startup; relevance: implements `openclaw gateway --port`/bind startup.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth gating at startup; relevance: enforces auth-required and the non-loopback bind refusal.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — graceful shutdown; relevance: implements the `shutdown` event before socket close (safety guarantee).
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: `gateway install` on macOS (LaunchAgent `ai.openclaw.gateway`).
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: Linux user/system `openclaw-gateway.service` install.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — Windows Scheduled Task render; relevance: native-Windows `OpenClaw Gateway` managed startup.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/env; relevance: `loginctl enable-linger` persistence after logout.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — restart handoff (bootout); relevance: `gateway restart`/`gateway stop` launchctl bootout semantics.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair path; relevance: `openclaw doctor --fix` service-drift repair.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: maps to `unauthorized`/`EADDRINUSE` common failure signatures.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: supervised-run reliability the runbook recommends.

### oc_gateway_runtime_protocol (9t · 11s · 11d)

**Terms** (9)
- [term_websocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: the single multiplexed port carries WS control/RPC.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — request/response RPC; relevance: operator protocol is `req(method,params)` → `res(ok|error)`.
- [term_rpc](../../term_dictionary/term_rpc.md) — remote procedure call; relevance: the gateway's method-call control plane.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw's own runtime model.
- [term_api_gateway](../../term_dictionary/term_api_gateway.md) — API fronting layer; relevance: the OpenAI-compatible HTTP surface (`/v1/*`) is an API-gateway role.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity check; relevance: all HTTP/WS surfaces share the trusted operator auth boundary.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `/tools/invoke` exposes tools over HTTP.
- [term_sse](../../term_dictionary/term_sse.md) — server-sent events streaming; relevance: agent runs stream `agent` events between accepted-ack and final response.
- [term_websocket_framing](../../term_dictionary/term_websocket_framing.md) — WS frame structure; relevance: first client frame MUST be `connect`; invalid first frames are rejected/closed.

**Docs** (11; ≥5 existing)
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — pi RPC protocol; relevance: direct analog of the connect→hello-ok→req/res handshake.
- [pi_rpc_events](../pi/pi_rpc_events.md) — pi RPC events; relevance: analog of OpenClaw's `agent`/`chat`/`session.*` event catalog.
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — pi RPC commands; relevance: analog of the method/request surface.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: analog of an OpenAI-compatible endpoint front end.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — pi streaming API; relevance: analog of the two-stage streamed agent-run response.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: operational counterpart that drives this runtime.
- [oc_network](oc_network.md) — (planned, this series) network hub; relevance: port/bind precedence + loopback-first model.
- [oc_logging_surfaces](oc_logging_surfaces.md) — (planned, this series) WS log surface; relevance: the Gateway WebSocket protocol log records RPC traffic.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) nodes; relevance: nodes connect to the same WS port with `role:"node"`.
- [oc_logging_configuration](oc_logging_configuration.md) — (planned, this series) trace correlation; relevance: HTTP/WS requests establish the internal request trace scope.
- [oc_help](oc_help.md) — (planned, this series) help hub; relevance: protocol-handshake debugging is a get-unstuck path.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: implements the multiplexed control plane + HTTP/WS endpoints.

**Snippets** (11)
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: the connect handshake + first-frame validation.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: `req`/`res` envelope structure.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — error codes/version; relevance: `res(error)` codes + protocol version negotiation.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — method/event schema groups; relevance: the conservative `features.methods`/`events` discovery list.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin routing; relevance: optional `/api/v1/admin/rpc` plugin route on the main port.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP message build; relevance: `/v1/chat/completions` request handling.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI SSE stream; relevance: streamed `/v1/*` responses.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — `/v1/responses` SSE; relevance: the agent-native responses endpoint.
- [snippet_openclaw_gateway_openresponses_tools_usage](../../code_snippets/snippet_openclaw_gateway_openresponses_tools_usage.md) — responses tools usage; relevance: `/tools/invoke` tool surface.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback MCP HTTP; relevance: loopback-default bind for the HTTP surface.

### oc_help (8t · 10s · 11d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: this is OpenClaw's own symptom-first help index.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness; relevance: doctor + gateway-status checks are the primary get-unstuck path.
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: "Install sanity" links Node/npm/PATH checks.
- [term_npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: install-sanity covers npm global-prefix/PATH issues.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: first-run FAQ covers auth/subscription failures.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: Models FAQ covers model selection/failover/auth profiles.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — fallback across models; relevance: Models FAQ is the documented home of failover guidance.
- [term_runbook](../../term_dictionary/term_runbook.md) — operational doc; relevance: help indexes the troubleshooting/doctor runbooks.

**Docs** (11; ≥5 existing)
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — Claude Code config debugging; relevance: analog of the diagnostics/environment-variable help cluster.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth troubleshooting; relevance: analog of first-run auth/subscription FAQ.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: analog of the install-sanity get-unstuck path.
- [pi_quickstart](../pi/pi_quickstart.md) — pi quickstart; relevance: analog of the "what do I click/run" first-time path.
- [hermes_faq_install_provider_terminal](../hermes_agent/hermes_faq_install_provider_terminal.md) — hermes FAQ; relevance: analog FAQ covering install/provider/terminal failures.
- [oc_install](oc_install.md) — (planned, this series) install; relevance: "Install sanity" link target.
- [oc_logging_surfaces](oc_logging_surfaces.md) — (planned, this series) logs; relevance: "Debugging" path uses watch-mode/raw streams.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: gateway-troubleshooting / local-vs-tailnet access path.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook/doctor; relevance: doctor + automated repair bundle.
- [oc_logging_configuration](oc_logging_configuration.md) — (planned, this series) diagnostics flags; relevance: diagnostics/verbose-mode help entries.
- [oc_date_time](oc_date_time.md) — (planned, this series) time handling; relevance: time-formatting debugging is a help-linked symptom.

**Repos** (2)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella; relevance: home of doctor/CLI/help surfaces.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: gateway-troubleshooting + doctor live here.

**Snippets** (10)
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor repair; relevance: the doctor automated-repair path help points to.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor preview/bundle; relevance: doctor diagnostic-bundle behavior.
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command catalog; relevance: the runnable commands the help index points at.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: how `openclaw help`/subcommands dispatch.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: first-run "what do I run" path.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect errors; relevance: gateway-troubleshooting symptom codes help routes to.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — analog doctor/auth-dir checks; relevance: analog of install-sanity/doctor diagnostics.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — CLI root guard; relevance: common first-run environment guard (a documented gotcha).
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup wizard config; relevance: onboarding/first-run path the help hub links.

### oc_install (9t · 11s · 11d)

**Terms** (9)
- [term_node_js](../../term_dictionary/term_node_js.md) — Node.js runtime; relevance: system requirement is Node 24 / 22.19+.
- [term_npm](../../term_dictionary/term_npm.md) — npm package manager; relevance: `npm install -g openclaw@latest` + global-prefix PATH fix.
- [term_docker](../../term_dictionary/term_docker.md) — containerization; relevance: Docker/Podman containerized install + Docker-VM hosting targets.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: this installs OpenClaw itself.
- [term_typescript](../../term_dictionary/term_typescript.md) — TS toolchain; relevance: from-source build (`pnpm build`/`ui:build`) of the TS codebase.
- [term_homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: analog system package-manager install path on macOS.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled background jobs; relevance: `--install-daemon` registers a managed background service.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: onboarding configures auth profiles post-install.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS gateway transport; relevance: `gateway status` post-install verifies the WS control plane is up.

**Docs** (11; ≥5 existing)
- [cc_install](../claude_code/cc_install.md) — Claude Code install; relevance: direct analog of multi-OS coding-agent install.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — advanced install + verify; relevance: analog of the "verify the install" + alternative-method section.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: analog of the `openclaw not found` PATH troubleshooting.
- [pi_containerization](../pi/pi_containerization.md) — pi containerization; relevance: analog of the Docker/Podman/container install paths.
- [hermes_installation](../hermes_agent/hermes_installation.md) — hermes install; relevance: analog cross-OS installer/npm/source install matrix.
- [hermes_install_windows_native](../hermes_agent/hermes_install_windows_native.md) — hermes Windows native; relevance: analog of the native-Windows/PowerShell installer path.
- [hermes_install_windows_wsl2](../hermes_agent/hermes_install_windows_wsl2.md) — hermes WSL2; relevance: analog of the WSL2 gateway install path.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: post-install `gateway install`/`status` verification.
- [oc_help](oc_help.md) — (planned, this series) help; relevance: install-sanity get-unstuck path.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: hosting/VPS deployment targets and bind config.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) node host; relevance: `openclaw node install` reuses the same daemon-install machinery.

**Repos** (3)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella + published package; relevance: the `openclaw` npm package + installer scripts.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboard/wizard; relevance: the onboarding flow launched by the installer.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — native apps; relevance: the native Windows/Mac Hub companion apps.

**Snippets** (11)
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: entry point that `openclaw --version`/`doctor` invoke post-install.
- [snippet_openclaw_cli_run_main_primary](../../code_snippets/snippet_openclaw_cli_run_main_primary.md) — primary CLI run path; relevance: the installed binary's main command dispatch.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: the onboarding the installer launches.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard imports; relevance: onboarding module wiring.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — onboarding prompts; relevance: interactive onboarding (`--no-onboard` skips this).
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: the migrate-on-install path.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist; relevance: macOS `--install-daemon` LaunchAgent.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit; relevance: Linux/WSL2 `--install-daemon` user service.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — Scheduled Task; relevance: native-Windows managed-startup install.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — root guard; relevance: install-time environment guard / PATH gotcha.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — analog install/doctor dirs; relevance: analog of post-install `openclaw doctor` checks.

### oc_logging_surfaces (8t · 11s · 11d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw's own log surfaces.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: Gateway WebSocket protocol logging for RPC traffic.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC; relevance: `openclaw logs --follow` tails the file log via `logs.tail` RPC.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness; relevance: "Gateway not reachable? Run `openclaw doctor`" troubleshooting tip.
- [term_pii](../../term_dictionary/term_pii.md) — personally identifiable info; relevance: log records omit transcript/audio payloads, only bounded metadata.
- [term_llm](../../term_dictionary/term_llm.md) — model; relevance: model-call lifecycle log records appear in the same file pipeline.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: tool-event payloads are part of the structured log entries.
- [term_observability_agent_systems](../../term_dictionary/term_observability_agent_systems.md) — observability for agent systems; relevance: file/console/WS log surfaces are the agent's primary observability inputs.

**Docs** (11; ≥5 existing)
- [cc_otel_audit_and_siem](../claude_code/cc_otel_audit_and_siem.md) — audit/SIEM via OTEL; relevance: analog of routing structured logs to external processors.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/data usage; relevance: analog of bounded, content-omitting log records.
- [cc_otel_events_reference](../claude_code/cc_otel_events_reference.md) — OTEL events reference; relevance: analog of the typed log-event catalog.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — hermes gateway ops; relevance: analog of where/how to read gateway logs.
- [pi_security_model](../pi/pi_security_model.md) — pi security model; relevance: analog of log-redaction / content-omission posture.
- [oc_logging_configuration](oc_logging_configuration.md) — (planned, this series) config; relevance: companion note on levels/redaction/diagnostics.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: `openclaw logs --follow` is in the verify/troubleshoot ladder.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) runtime; relevance: WS protocol logging records the RPC traffic.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: Control UI Logs tab is a web surface bound to the gateway.
- [oc_help](oc_help.md) — (planned, this series) help; relevance: "find logs quickly" is a documented help path.
- [oc_date_time](oc_date_time.md) — (planned, this series) time; relevance: log file date + `--local-time` use the same timezone selection.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: implements the file-JSONL/console/WS log pipeline.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella + CLI; relevance: home of `openclaw logs`/`channels logs` commands.

**Snippets** (11)
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — analog `logs` CLI; relevance: analog of `openclaw logs --follow` tailing implementation.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — analog logging setup; relevance: analog of the JSONL file-log writer config.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered delta/heartbeat; relevance: bounded lifecycle records flowing through the log pipeline.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk/voice lifecycle; relevance: talk/realtime-voice records emit bounded log entries (no transcript text).
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency accounting; relevance: model-call size/timing fields surfaced in logs.
- [snippet_openclaw_gateway_channels_runtime_snapshot](../../code_snippets/snippet_openclaw_gateway_channels_runtime_snapshot.md) — channel runtime snapshot; relevance: `channels logs --channel` channel-only filtering.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status; relevance: per-channel activity that channel-only logs surface.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection; relevance: Gateway WebSocket protocol logging hooks here.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: WS request/response traffic that `--verbose --ws-log` renders.

### oc_logging_configuration (9t · 11s · 11d)

**Terms** (9)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw's own `logging.*` config.
- [term_pii](../../term_dictionary/term_pii.md) — PII; relevance: redaction of payment/secret fields (card number, CVC, payment token).
- [term_pci](../../term_dictionary/term_pci.md) — payment-card security; relevance: built-in defaults redact card number / CVC/CVV / payment credentials.
- [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — cache accounting; relevance: model-call diagnostics record bounded request/response sizes (cache-relevant).
- [term_sse](../../term_dictionary/term_sse.md) — streamed events; relevance: `OPENCLAW_DEBUG_SSE=events|peek` emits first-event/stream-completion timing.
- [term_llm](../../term_dictionary/term_llm.md) — model; relevance: `OPENCLAW_DEBUG_MODEL_*` targets provider/model-transport logs.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: `MODEL_PAYLOAD=tools` logs model-facing tool names.
- [term_context_propagation](../../term_dictionary/term_context_propagation.md) — trace-context propagation; relevance: traceId/spanId/traceparent join logs with OTEL spans.
- [term_trace](../../term_dictionary/term_trace.md) — distributed trace; relevance: HTTP/WS request trace scope + agent/model child traces.

**Docs** (11; ≥5 existing)
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTEL setup; relevance: analog of enabling diagnostics/OTLP export.
- [cc_otel_configuration_variables](../claude_code/cc_otel_configuration_variables.md) — OTEL config vars; relevance: analog of `diagnostics.otel.*` + env overrides.
- [cc_otel_traces](../claude_code/cc_otel_traces.md) — OTEL traces; relevance: analog of traceId/spanId trace correlation.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — OTEL privacy model; relevance: analog of bounded-attribute, content-omitting telemetry.
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK observability; relevance: analog of model-call spans/metrics from log diagnostics.
- [oc_logging_surfaces](oc_logging_surfaces.md) — (planned, this series) surfaces; relevance: companion note (where logs live / how to read).
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) runtime; relevance: request-trace scope established by HTTP/WS frames.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: `--log-level`/`--verbose` operator flags.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: OTLP export to remote collectors crosses the network boundary.
- [oc_nodes_command_policy](oc_nodes_command_policy.md) — (planned, this series) policy; relevance: redaction of exec command display + safety-boundary payloads.
- [oc_help](oc_help.md) — (planned, this series) help; relevance: diagnostics-flags help entry.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: implements logging config + OTEL export + diagnostics flags.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security repo; relevance: the always-on safety-boundary redaction that `redactSensitive:"off"` cannot disable.

**Snippets** (11)
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — analog redact patterns; relevance: analog of `redactPatterns` regex masking.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: the secret values redaction targets.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security audit composition; relevance: safety-boundary payload redaction always-on.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency; relevance: `requestPayloadBytes`/`durationMs`/`timeToFirstByteMs` model-call timing.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost summary; relevance: bounded model-call measurements feeding diagnostics.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — SSE stream; relevance: `OPENCLAW_DEBUG_SSE` first-event/stream-completion timing.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk lifecycle; relevance: talk records flow to diagnostics-otel log export.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — analog logging setup; relevance: analog of `logging.level`/`consoleLevel` config.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: WS-log verbose rendering of request/response.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — model-fallback observation logging; relevance: model-transport diagnostics surface these observations.

### oc_nodes_pairing_host (9t · 12s · 11d)

**Terms** (9)
- [term_websocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: nodes connect to the gateway WS with `role:"node"`.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw node pairing + node host.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: `OPENCLAW_GATEWAY_TOKEN` over the SSH tunnel for node-host auth.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: node-host auth fails closed if `gateway.auth.*` SecretRefs are unresolved.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: node `system.run` is gated by exec approvals + file-operand binding.
- [term_access_control](../../term_dictionary/term_access_control.md) — authorization scopes; relevance: approval scopes escalate (`operator.pairing`→`+write`→`+admin`) by declared commands.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC; relevance: `node.invoke` / `nodes invoke` are RPC calls to the node.
- [term_dm_pairing](../../term_dictionary/term_dm_pairing.md) — device/DM pairing handshake; relevance: nodes present a device identity during `connect` creating a pairing request.
- [term_device_id](../../term_dictionary/term_device_id.md) — device identity; relevance: device pairing record is the durable approved-role contract per node id.

**Docs** (11; ≥5 existing)
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox isolation; relevance: analog of node exec-approval + file-operand binding isolation.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission precedence; relevance: analog of the pairing approval-scope escalation model.
- [pi_security_model](../pi/pi_security_model.md) — pi security model; relevance: analog of remote-exec auth + approval posture.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH; relevance: direct analog of token-bearing connection through an SSH tunnel.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote auth; relevance: analog of connecting a remote host to a loopback-bound gateway.
- [oc_nodes_capabilities](oc_nodes_capabilities.md) — (planned, this series) capabilities; relevance: the command surface a paired node host exposes.
- [oc_nodes_command_policy](oc_nodes_command_policy.md) — (planned, this series) policy; relevance: the two-gate policy enforced on the paired node's commands.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: pairing/identity + loopback-bind + SSH-tunnel posture.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: the gateway host nodes pair to.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) protocol; relevance: `connect` handshake + `role:"node"` declaration.
- [oc_install](oc_install.md) — (planned, this series) install; relevance: `openclaw node install` reuses the daemon-install machinery.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: device-pairing store + node forwarding (`exec host=node`).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella + CLI; relevance: `openclaw node run/install` + `devices`/`nodes` CLIs.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security repo; relevance: exec-approvals enforcement on the node host.

**Snippets** (12)
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: implements the device-pairing request/approve flow.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS node pairing; relevance: the device-identity handshake for a mobile node.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android node WS session; relevance: a node connecting over WS with role node.
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — Android mDNS discovery; relevance: node discovery before pairing on local network.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session kit; relevance: node-host session lifecycle against the gateway.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: `--tls`/`--tls-fingerprint` node-host secure connect.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: `~/.openclaw/exec-approvals.json` allowlist enforcement.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — exec approval push; relevance: approval prompts routed to a node device.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: `system.run` plan + concrete-file-operand binding.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret resolution; relevance: node-host auth via `OPENCLAW_GATEWAY_*` / SecretRefs fail-closed.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: connecting through the SSH-tunnel loopback endpoint.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — service unit render; relevance: `openclaw node install`/`node start` headless-host service.

### oc_nodes_capabilities (9t · 12s · 11d)

**Terms** (9)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw node capability/command surface.
- [term_sms](../../term_dictionary/term_sms.md) — short message service; relevance: Android nodes expose `sms.send`/`sms.search` with SMS permission.
- [term_geofence](../../term_dictionary/term_geofence.md) — location services; relevance: `location.get` returns lat/lon/accuracy with precise/max-age options.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: talk/push-to-talk node commands feed transcription.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: talk-capable nodes render voice output.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-format media; relevance: canvas snapshots, camera photos/clips, screen recordings become MEDIA agent context.
- [term_browser_automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: `canvas.navigate`/`canvas.eval`/`canvas.present` drive a WebView.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC; relevance: `nodes invoke --command … --params` is raw node RPC.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: node commands surface to the agent as callable tools.

**Docs** (11; ≥5 existing)
- [cc_tools_catalog](../claude_code/cc_tools_catalog.md) — agent tools catalog; relevance: analog of the node-command-as-tool surface.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode; relevance: analog of the talk/voice node capability.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice CLI; relevance: analog of push-to-talk CLI commands.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation; relevance: analog of canvas WebView navigate/eval.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — custom tools; relevance: analog of exposing device commands as agent tools.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) pairing/host; relevance: a node must be paired before its commands are invocable.
- [oc_nodes_command_policy](oc_nodes_command_policy.md) — (planned, this series) policy; relevance: each capability is gated by the two-gate command policy.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: nodes-as-peripherals + transports.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) protocol; relevance: `node.invoke` rides the WS RPC plane.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: gateway routes node-command tool calls.
- [oc_help](oc_help.md) — (planned, this series) help; relevance: node-crash/permission troubleshooting paths.

**Repos** (3)
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — native apps; relevance: mac/iOS/Android apps expose canvas/camera/screen/device commands.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone; relevance: talk/voice node surface (push-to-talk, transcription).
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella + CLI; relevance: `openclaw nodes …` helper commands.

**Snippets** (12)
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: implements `nodes invoke`/`node.invoke` dispatch.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — Android invoke dispatcher; relevance: dispatches device/sms/notifications/photos commands on Android nodes.
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — canvas lifecycle; relevance: `canvas.snapshot`/`present`/`navigate` WebView control.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — canvas file watcher; relevance: A2UI/canvas content updates rendered on the node.
- [snippet_openclaw_macos_pushtotalk_overlay](../../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md) — push-to-talk overlay; relevance: `talk.ptt.*` node commands.
- [snippet_openclaw_macos_pushtotalk_nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — PTT key events; relevance: push-to-talk start/stop/cancel triggers.
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — voice-wake trigger; relevance: talk-capability node voice activation.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: camera/canvas snapshot `--max-width`/`--quality` handling.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — media record lifecycle; relevance: photo/clip/screen-record MEDIA-line emission.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — STT pipeline; relevance: talk-node transcription path.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — TTS pipeline; relevance: talk-node voice output.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: node media becomes agent transcript MEDIA attachments.

### oc_nodes_command_policy (9t · 11s · 11d)

**Terms** (9)
- [term_access_control](../../term_dictionary/term_access_control.md) — authorization; relevance: the two-gate check (node `connect.commands` AND gateway platform policy).
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: dangerous commands (`camera.snap`/`screen.record`/`system.run`) require opt-in + exec-approval gating.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: command-policy applies to authenticated paired nodes only.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: documents OpenClaw's node command-policy model + `gateway.nodes` schema.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS; relevance: nodes declare allowed commands in the WS `connect.commands` list.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: plugin node-invoke policy applies to raw invoke, CLI helpers, and agent tools alike.
- [term_pii](../../term_dictionary/term_pii.md) — PII; relevance: privacy-heavy commands (camera/screen/contacts) require explicit opt-in.
- [term_cidr](../../term_dictionary/term_cidr.md) — IP range notation; relevance: `pairing.autoApproveCidrs` auto-approves first-time node pairing from trusted CIDRs.
- [term_dm_pairing](../../term_dictionary/term_dm_pairing.md) — device/DM pairing handshake; relevance: after a node changes its declared command list, the old pairing is rejected so the gateway re-snapshots the policy.

**Docs** (11; ≥5 existing)
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission precedence; relevance: direct analog of allow/deny precedence (deny-wins).
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permissions; relevance: analog of the gate between declared capability and platform policy.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — permission rules; relevance: analog of the rule-based command allowlist/denylist.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool rules; relevance: analog of exact-command-name allow/deny.
- [pi_security_model](../pi/pi_security_model.md) — pi security model; relevance: analog of the two-layer authorization model.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) pairing/host; relevance: pairing approval scopes feed the policy gate.
- [oc_nodes_capabilities](oc_nodes_capabilities.md) — (planned, this series) capabilities; relevance: the commands this policy gates.
- [oc_network](oc_network.md) — (planned, this series) network; relevance: CIDR auto-approve operates on the network-trust boundary.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) protocol; relevance: `connect.commands` declaration in the handshake.
- [oc_logging_configuration](oc_logging_configuration.md) — (planned, this series) logging; relevance: exec command display is redacted at the safety boundary.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: `gateway.nodes`/`tools.exec` config lives in the gateway config.

**Repos** (2)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security repo; relevance: command allow/deny policy + exec approvals enforcement.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: platform policy + plugin node-invoke gate.

**Snippets** (11)
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: implements the two-gate allow/deny check (deny-wins).
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: where the policy gate runs before forwarding.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tools deny; relevance: the dangerous/privacy-heavy command opt-in defaults.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: per-method authorization gate analog.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: re-approval after a node changes its declared command snapshot.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing allowlist/CIDR; relevance: `autoApproveCidrs` first-time auto-approve.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: `system.run` opt-in needs `operator.admin` + exec approvals.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: `system.run` policy enforcement.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: auditing dangerous command execution.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec dedup; relevance: plugin node-invoke policy boundary across surfaces.

### oc_network (9t · 11s · 11d)

**Terms** (9)
- [term_websocket](../../term_dictionary/term_websocket.md) — WS control plane; relevance: gateway WS defaults to `ws://127.0.0.1:18789` (loopback first).
- [term_vpn](../../term_dictionary/term_vpn.md) — VPN; relevance: remote access is typically Tailscale VPN or SSH tunnel.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: non-loopback binds require a valid gateway auth path.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: `trusted-proxy` non-loopback deployment option.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the product; relevance: this is OpenClaw's network architecture/security hub.
- [term_access_control](../../term_dictionary/term_access_control.md) — authorization; relevance: tailnet/LAN clients require explicit pairing approval (local-trust auto-approve only on loopback).
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC; relevance: the WS control plane carries RPC + canvas on the same port.
- [term_bonjour_discovery](../../term_dictionary/term_bonjour_discovery.md) — Bonjour/mDNS discovery; relevance: discovery + transports section lists Bonjour/mDNS.
- [term_dm_pairing](../../term_dictionary/term_dm_pairing.md) — device/DM pairing; relevance: pairing + identity (DM + node) is a core network concept.

**Docs** (11; ≥5 existing)
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network TLS/access; relevance: analog of bind/access + TLS posture.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud network access; relevance: analog of remote/non-loopback access control.
- [pi_security_model](../pi/pi_security_model.md) — pi security model; relevance: analog of loopback-first + auth-required posture.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote auth; relevance: analog of securing remote/tailnet access.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth over SSH; relevance: analog of SSH-tunnel remote access.
- [oc_gateway_runbook](oc_gateway_runbook.md) — (planned, this series) runbook; relevance: the gateway process this hub describes.
- [oc_gateway_runtime_protocol](oc_gateway_runtime_protocol.md) — (planned, this series) runtime; relevance: single multiplexed WS port + bind modes.
- [oc_nodes_pairing_host](oc_nodes_pairing_host.md) — (planned, this series) nodes; relevance: nodes-as-peripherals + transports section.
- [oc_nodes_command_policy](oc_nodes_command_policy.md) — (planned, this series) policy; relevance: CIDR auto-approve operates on the trust boundary.
- [oc_install](oc_install.md) — (planned, this series) install; relevance: hosting/VPS deployment + bind config.
- [oc_help](oc_help.md) — (planned, this series) help; relevance: local-vs-tailnet access debugging is a help path.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway repo; relevance: WS control plane + bind modes + canvas-on-same-port.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security repo; relevance: auth/pairing + loopback-first posture.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — umbrella; relevance: top-level home of the networking docs surfaced here.

**Snippets** (11)
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — listener + bind; relevance: loopback-default WS bind on `127.0.0.1:18789`.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth at startup; relevance: non-loopback bind requires a valid auth path.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth modes; relevance: token/password vs trusted-proxy auth modes.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/proxy; relevance: trusted-proxy / tunnel client connection.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: identity-bearing connect over secured transports.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: tailnet/LAN pairing approval vs loopback auto-approve.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: pairing + identity local-trust model.
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS discovery; relevance: Bonjour/mDNS discovery + transports.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: securing non-loopback transports.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP; relevance: canvas/HTTP surfaces on the same loopback port.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security audit; relevance: the loopback-first/auth-required security posture this hub summarizes.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc content (its home is this sub-plan), and existing
`term_dictionary` terms are LINKED, never inlined. Expected **0 new `term_dictionary` captures** for rt02.

| Term (appears in source) | Disposition |
|---|---|
| Gateway, node, node host, headless node host, Mac node mode | OpenClaw product vocabulary → digested as `oc_gateway_*` / `oc_nodes_*` doc content; not term notes. Anchor concepts link `term_openclaw`. |
| envelopeTimezone / userTimezone / timeFormat / IANA timezone | Config-field vocabulary → `oc_date_time` content. No `term_timezone` note exists; do NOT inline a definition, link `term_openclaw`; concept of timezone is self-explanatory in context. |
| OpenAI-compatible endpoints (`/v1/models`, `/v1/embeddings`, `/v1/chat/completions`, `/v1/responses`) | API-surface vocabulary → `oc_gateway_runtime_protocol` content; link existing `term_api_gateway` + `term_function_calling` (`/tools/invoke`). |
| WebSocket control plane / connect→hello-ok→req/res protocol | Link existing `term_websocket`, `term_json_rpc`, `term_rpc`; protocol detail digested in `oc_gateway_runtime_protocol`. |
| device pairing / approval scopes / token rotation | Link existing `term_access_control` + `term_authentication` + `term_oauth_token`; digested in `oc_nodes_pairing_host` / `oc_network`. No `term_device_pairing` note exists; not promoted (single-product concept, no cross-cutting reuse). |
| launchd / systemd / Scheduled Task supervision | Platform-supervisor vocabulary → `oc_gateway_runbook` content. No `term_systemd`/`term_launchd` notes exist; not promoted (OS-native, low cross-vault reuse), described inline in the runbook. |
| Node / npm / pnpm / bun / Docker / Podman / Nix / Ansible / Kubernetes install paths | Link existing `term_node_js`, `term_npm`, `term_docker`; remaining package managers/cloud targets are config-only mentions, not term notes. |
| JSONL file logs / console styles / `OPENCLAW_DEBUG_*` flags / redaction | Logging vocabulary → `oc_logging_*` content; link existing `term_pii` (redacted payment/secret fields). No `term_logging`/`term_redaction` notes exist; not promoted. |
| OpenTelemetry / OTLP / traceId/spanId/traceparent / diagnostics | Link existing analog docs (`cc_otel_*`); no `term_opentelemetry` note exists. Not promoted here — if a cross-cutting OTEL term is warranted it is owned corpus-wide, not by rt02 (master expects near-0). |
| Tailscale / tailnet / SSH tunnel / loopback bind | Link existing `term_vpn`; digested in `oc_network` / `oc_gateway_runbook`. No `term_tailscale`/`term_ssh_tunnel`/`term_loopback` notes; not promoted (link `term_vpn` + describe inline). |
| canvas / A2UI / camera / screen recording / location / SMS / device commands | Node capability vocabulary → `oc_nodes_capabilities` content; link existing `term_sms`, `term_geofence` (location), `term_speech_to_text`/`term_text_to_speech` (talk). No `term_canvas`/`term_camera` notes; not promoted (product-specific surfaces). |

**New-term candidates:** none. No genuinely reusable cross-cutting term lacking an existing note AND lacking a
doc-page home was found. (If augment's Step 2d re-scan surfaces one, e.g. a generic "node host" or
"OpenAI-compatible API" concept with vault-wide reuse, capture via `/tessellum-capture-term-note` + add to the
best-fit `acronym_glossary_*.md` — most likely `acronym_glossary_a.md` for "API" or the agentic/LLM glossary.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** rt02 authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format: YAML field order + body structure (Overview / mirrored H2 / Related Notes / References / bold footer); ≤400L / ≤2500w / ≤6 code / one BB | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: digest claims diff-checked vs `inbox/openclaw_docs/<page>.md` (no fabrication; config/CLI snippets reproduced verbatim) | manual diff vs mirror |
| G3 | Density + Coverage: every source H2/H3 maps to a note (Section Coverage Map); no over-compression; within caps | coverage map review + word/code recount |
| G4 | Cross-Reference: ≥6 relevance-selected term links + sibling `oc_*` + `repo_openclaw*` + other docs per note, each with a relevance statement | Related Notes review |
| G6 | Broken-link fix: relative paths resolve | `/tessellum-fix-broken-links` + reindex |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island) | inlink audit (via `entry_openclaw_docs.md`) |
| G8 | In-degree ≥1 per new note after reindex | `note_links` query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_date_time oc_gateway_runbook oc_gateway_runtime_protocol oc_help oc_install oc_logging_surfaces oc_logging_configuration oc_nodes_pairing_host oc_nodes_capabilities oc_nodes_command_policy oc_network"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"
  done
  # source_url required
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"
  fi
  # density caps (≤2500 words / ≤6 code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # sibling-prefix cross-ref present (at least one oc_ sibling link expected)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) LINK: $n"
done

# YAML frontmatter sweep across the whole folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# Ghost-reference (every cited note id must exist in DB)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
grep -rhoE '\]\(([^)]+\.md)\)' "$GATE_DIR"/oc_*.md | sed -E 's/.*\(([^)]+)\).*/\1/' | xargs -n1 basename | sort -u | \
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_date_time | procedure | 500 | ≤6 | ✅ |
| 2 | oc_gateway_runbook | procedure | 700 | ≤6 | ✅ |
| 3 | oc_gateway_runtime_protocol | concept | 650 | ≤4 | ✅ |
| 4 | oc_help | concept | 350 | 0 | ✅ |
| 5 | oc_install | procedure | 650 | ≤6 | ✅ |
| 6 | oc_logging_surfaces | procedure | 650 | ≤6 | ✅ |
| 7 | oc_logging_configuration | procedure | 700 | ≤6 | ✅ |
| 8 | oc_nodes_pairing_host | procedure | 700 | ≤6 | ✅ |
| 9 | oc_nodes_capabilities | procedure | 700 | ≤6 | ✅ |
| 10 | oc_nodes_command_policy | concept | 550 | ≤3 | ✅ |
| 11 | oc_network | concept | 350 | 0 | ✅ |

No note approaches the 400-line / 2,500-word / 6-code caps. The three code-heavy/mixed pages (`nodes.md` 25
fences, `gateway.md` 15, `logging.md` 8) were split precisely so each digest note reproduces only ≤6 load-bearing
snippets verbatim and carries a single building block.

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before any sub-plan
executes) under a **Top-level / Operational core** cluster: gateway (runbook + runtime/protocol), install, logging
(surfaces + configuration), nodes (pairing/host + capabilities + command-policy), network, date-time, help. Each
new note receives its entry-point back-link at finalization (satisfies G7/G8). Parent-hub wiring
`repo_openclaw.md`) are master-level W2/W3 steps.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; ≥1 per new note for G7/G8):

- `entry_openclaw_docs.md` (created W1) → **all 11 notes** (primary anti-island guarantee).
- `repo_openclaw_gateway.md` → oc_gateway_runbook, oc_gateway_runtime_protocol, oc_logging_surfaces,
  oc_logging_configuration, oc_network, oc_nodes_pairing_host, oc_nodes_command_policy.
- `repo_openclaw_security.md` → oc_network, oc_nodes_command_policy, oc_nodes_pairing_host, oc_logging_configuration.
- `repo_openclaw_agents.md` → oc_date_time.
- `repo_openclaw_apps.md` → oc_install, oc_nodes_capabilities.
- `repo_openclaw_cli_wizard.md` → oc_install.
- `repo_openclaw.md` → oc_install, oc_help, oc_gateway_runbook.
- `term_openclaw.md` → oc_gateway_runbook, oc_install, oc_network (code↔docs back-link, master W3).
- `term_websocket.md` → oc_gateway_runtime_protocol, oc_network, oc_nodes_pairing_host.
- `term_vpn.md` → oc_network, oc_gateway_runbook.
- `term_access_control.md` → oc_nodes_command_policy.

## Pacing Rules (inherited from master)

Single execution phase; 8 gates before commit. Re-read each source page during execution; reproduce config/CLI
snippets verbatim; one BB per note. Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the
script; reindex incrementally; verify `note_links` + 0 broken links before commit. `git pull --rebase --autostash`
first; commit + push per wave; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping LOCKED at raised floors; see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 PASS, READY (see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (plan `status: ready`) |

## Augmentation Report (2026-06-21)

**Scope of this pass:** xref-augment — built and LOCKED the per-note Related Notes mapping at the RAISED
floors (**≥8 terms · ≥10 code_snippets · ≥10 docs per note**), replacing the PLAN-stage `## Candidate
Cross-References` (≥6-term sketch) with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.
All 7 source pages were re-read from the `inbox/openclaw_docs/` mirror (measured words match the Source table
exactly: date-time 503 · gateway 1,563 · help 213 · install 819 · logging 1,715 · network 313 · nodes 2,632 =

**What was locked (per-note counts; floors met = all 11):**

| Note | Terms | Snippets | Docs (existing/planned-oc) | Repos | Floors |
|---|---:|---:|---:|---:|---|
| oc_date_time | 8 | 10 | 11 (5/6) | 2 | ✅ |
| oc_gateway_runbook | 9 | 11 | 11 (5/6) | 3 | ✅ |
| oc_gateway_runtime_protocol | 9 | 11 | 11 (5/6) | 2 | ✅ |
| oc_help | 8 | 10 | 11 (5/6) | 2 | ✅ |
| oc_install | 9 | 11 | 11 (7/4) | 3 | ✅ |
| oc_logging_surfaces | 8 | 11 | 11 (5/6) | 2 | ✅ |
| oc_logging_configuration | 9 | 11 | 11 (5/6) | 2 | ✅ |
| oc_nodes_pairing_host | 9 | 12 | 11 (5/6) | 3 | ✅ |
| oc_nodes_capabilities | 9 | 12 | 11 (5/6) | 3 | ✅ |
| oc_nodes_command_policy | 9 | 11 | 11 (5/6) | 2 | ✅ |
| oc_network | 9 | 11 | 11 (5/6) | 3 | ✅ |

docs + repos all OK; 111 snippet citations all present). A deterministic link sweep of the LOCKED section
planned sibling `oc_*` docs that THIS sub-plan creates (cited toward the ≥10-doc floor as "(planned, this
series)"). Within-note duplicate check: 0 duplicate terms, 0 duplicate snippets in any note.

`claude_code/cc_*` (≈339), `pi/pi_*` (42), `hermes_agent/hermes_*` (≈226); repos `repo_openclaw*` (15 verified)

**New-term candidates:** **NONE.** Per master + this sub-plan's `## Undigested Terms Plan`, OpenClaw vocabulary
is digested as `oc_*` doc content and existing `term_dictionary` terms are LINKED only (expected 0 new term
captures). The xref re-read surfaced no genuinely cross-cutting, vault-reusable term lacking BOTH an existing
note AND a doc-page home. Notably, several operational concepts that had NO term note at PLAN stage DO have one
and are now LINKED (re-scan found `term_runbook`, `term_model_failover`, `term_observability_agent_systems`,
`term_context_propagation`, `term_trace`, `term_dm_pairing`, `term_device_id`, `term_bonjour_discovery`,
`term_cidr`, `term_a2ui`, `term_pkce`, `term_multimodal`, `term_browser_automation`, `term_voip`,
`term_homebrew`, `term_typescript`, `term_pci`, `term_gdpr` — used where relevant), reducing reliance on the
"link the closest existing term" fallback. If a future enricher pass wants a single cross-cutting candidate, the
only borderline one is **"OpenAI-compatible API"** (best-fit glossary `acronym_glossary_a.md`) — but it is
adequately covered by `term_api_gateway` + the `oc_gateway_runtime_protocol` doc, so it is NOT promoted.

**Sections unchanged (inherited from PLAN, re-verified):** Scope, Source table (measured), Content Strategy,
Planned Notes, Section Coverage Map (0 orphans), Split Decisions (nodes→3, gateway→2, logging→2), Undigested
Terms Plan (0 new), Term-Note Authoring Requirements (N/A — 0 new terms; master mandate applies if any
surface), G1–G8 gate table, Validation Scripts (incl. ghost sweep), Density Re-Assessment (no note near caps),
Entry Point Decision (inherits `entry_openclaw_docs` created at master W1), Inlinks (≥1 outside-folder inbound
per note via `entry_openclaw_docs` + repos), Pacing Rules.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

PLAN REVIEW — FINAL SIGN-OFF · Plan: `plan_digest_openclaw_docs_rt02.md` · Date: 2026-06-21

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance statements) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 11 notes ≥8 terms (8/8/9 distribution), ≥10 snippets, ≥10 docs; every link carries `— <what> ; relevance: <why THIS note>`; 0 within-note dup terms/snippets. |
| CP2 | 9-GATE table per batch (G1–G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single execution phase; includes G1 format, G2 grounding (diff vs `inbox/openclaw_docs/`), G3 density+coverage, G4 cross-ref, G5 ghost detect+redirect, G6 broken-link fix, G7/G8 discoverability/in-degree. Validation Scripts include the ghost-reference sweep + YAML frontmatter check. |
| CP4 | Plan size manageable | **PASS** | 11 notes ≤ 30 (single execution phase); this is one sub-plan of the 105-sub-plan master split. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited from master `## Format Definition`, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (same source type: open-source coding-agent docs): `## Overview` opener, `## Related Notes` reference section, `**Source**`/`**Last Updated**`/`**Status**` footer, forbidden-field list. Target dir `resources/documentation/openclaw/` is new (sibling to verified analog dirs). |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: no note approaches 400-line/2,500-word/6-code caps (max ~700w). The 3 code-heavy/mixed pages were already split (nodes 2,632w→3, gateway 1,563w→2, logging 1,715w→2) so each digest note is single-BB and ≤6 load-bearing snippets. No unaddressed borderline. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 source pages re-read from `inbox/openclaw_docs/` this pass; `wc -w` matches the Source table exactly (7,758 total). Ratio measured/plan = 1.00 for every page. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (every OpenClaw-vocabulary row dispositioned to `oc_*` doc content or an existing-term link; **0 new captures**); `## Term-Note Authoring Requirements` present as N/A with the master multi-source-research mandate carried forward should any term surface. Must-language used. |
| CP8f | Term-slug + all-notes dedup/collision audit | **PASS** | 0 new term slugs to rename (0 captures), so no specificity collisions possible. All-notes collision audit: the 11 planned `oc_*` doc slugs were checked against `term_dictionary/` AND `resources/documentation/` — none duplicate an existing substantive note (openclaw doc folder is empty; OpenClaw concepts on the code side are repos/snippets/terms that this plan LINKS, not doc concept notes). PLAN's MISSING-stem note documents the closest-existing-term fallbacks. |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 11; plus `repo_openclaw_gateway`/`_security`/`_agents`/`_apps`/`_cli_wizard`/`repo_openclaw`, `term_openclaw`/`_websocket`/`_vpn`/`_access_control`). G8-Discoverability + in-degree≥1 present in the gate table as a gated execution step, not a recommendation. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan `status` advanced `pending → ready`.
