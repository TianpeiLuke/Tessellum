---
title: Sub-Plan B08B — Claude Code Docs: Channels
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["channels", "channels-reference"]
---

# Sub-Plan B08B: Channels

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 2 Channels pages: the user-facing guide for installing and running channels (`channels.md`) and the
build-your-own MCP-server contract reference (`channels-reference.md`). A **channel** is an MCP server
that *pushes* events (chat messages, webhooks, alerts) into a running Claude Code session so Claude can
react while you are away, optionally replying back through the same channel (two-way / chat bridge) and
relaying permission prompts to a remote device. P2 (Phase B) — builds on the MCP, permissions, and
plugins cores. The glossary term **Channel** is owned by B08B per the master's Pattern B and is digested
as the `cc_channels_overview` doc-concept note (not a new `term_dictionary` note).

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 8,240 measured words. **Planned: 6 notes.**

## Content Strategy

- **Prioritize**: the channel concept (push-vs-poll event model, two-way bridge) and the build-your-own
  contract (capability declaration, notification format, reply tool, permission relay) — these are what
  later surfaces (Remote Control B12B, Slack B13A, MCP B08A) cross-reference.
- **Group**: split `channels.md` by BB — the channel concept + comparison + research preview (concept),
  the per-platform install/quickstart steps (procedure), and the security/enterprise-controls config
  (procedure). Split `channels-reference.md` by buildable artifact — the base one-way webhook server
  (procedure/code), the two-way reply tool (procedure/code), and the permission-relay extension
  (procedure/code) — because each is a distinct walkthrough and the page's code volume blows the ≤6-code
  cap if kept whole.
- **Skip / link-out (own other sub-plans)**: plugin install / marketplace mechanics → B09A
  (`plugins.md`) / B09B (`plugin-marketplaces.md`); the underlying MCP protocol + `.mcp.json` →
  B08A (`mcp.md`); `--dangerously-skip-permissions` + permission modes → B05A (`permission-modes.md`);
  managed settings keys generally → B03A (`settings.md`) / B14B (`server-managed-settings.md`);
  Remote Control / Slack / web sessions / scheduled-tasks comparison rows → B12B / B13A / B12B / B11.
  These are referenced via links, never duplicated.
- **Glossary**: the **Channel** term routes to `cc_channels_overview` (doc concept, Pattern B); MCP /
  Subagent / Plugin / Permission-mode / Prompt-injection route to existing term notes or their home
  sub-plan (see Undigested Terms Plan). No new `term_dictionary` capture.

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| channels | /channels | 2,696 | 13 | 6 | 2 | concept + procedure |
| channels-reference | /channels-reference | 5,544 | 17 | 8 | 5 | procedure + model |

> **H2 lists (document order):**
> - **channels**: Supported channels (H3 Tabs: Telegram · Discord · iMessage) · Quickstart (fakechat) · Security · Enterprise controls (H3 Enable channels for your organization, Restrict which channel plugins can run) · Research preview · How channels compare · Next steps
> - **channels-reference**: Overview · What you need · Example: build a webhook receiver · Test during the research preview · Server options · Notification format · Expose a reply tool · Gate inbound messages · Relay permission prompts (H3 How relay works, Permission request fields, Add relay to a chat bridge, Full example) · Package as a plugin · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **6 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_channels_overview.md` | concept | channels: intro, How channels compare, Research preview; channels-reference: intro, Overview | 600 | What a channel is (an MCP server pushing events into a running session); one-way vs two-way / chat bridge; push-vs-poll event model; comparison to web sessions / Slack / MCP / Remote Control; research-preview status + version gate. Owns the glossary **Channel** term. |
| 2 | `cc_channels_setup.md` | procedure | channels: Supported channels (Telegram/Discord/iMessage tabs), Quickstart (fakechat) | 600 | Install + run a pre-built channel: Bun prereq, `/plugin install`, `--channels` flag, per-platform bot creation + pairing (Telegram/Discord) and Full-Disk-Access/self-chat (iMessage); fakechat localhost demo. Plugin/marketplace mechanics → B09A/B09B. |
| 3 | `cc_channels_security_and_enterprise_controls.md` | procedure | channels: Security, Enterprise controls (+ both H3) | 500 | Sender allowlist + pairing bootstrap; `--channels` opt-in gate (being in `.mcp.json` is not enough); `channelsEnabled` master switch + `allowedChannelPlugins` plugin restriction (managed-settings JSON); permission-relay allowlist note. Managed-settings layering → B03A/B14B. |
| 4 | `cc_build_a_channel.md` | procedure | channels-reference: What you need, Example: build a webhook receiver, Server options, Notification format, Test during the research preview, Package as a plugin | 700 | Build a one-way channel: requirements (MCP SDK + Node-compatible runtime), the three server obligations (declare `claude/channel`, emit `notifications/claude/channel`, connect over stdio), minimal `webhook.ts`, `Server` constructor option table, `<channel>` notification payload (`content`/`meta`), dev flag + `.mcp.json` registration, packaging as a plugin. |
| 5 | `cc_channel_reply_tool.md` | procedure | channels-reference: Expose a reply tool | 450 | Make a channel two-way: add `tools: {}` capability, register a `reply` MCP tool (ListTools/CallTool handlers + inputSchema), `instructions` routing (pass `chat_id` back); SSE-stream outbound for local curl testing. |
| 6 | `cc_channel_permission_relay.md` | procedure | channels-reference: Relay permission prompts (+ How relay works, Permission request fields, Add relay to a chat bridge, Full example), Gate inbound messages | 700 | Relay tool-approval prompts to a remote device: `claude/channel/permission` capability, the 4-step relay loop, `permission_request` fields (`request_id`/`tool_name`/`description`/`input_preview`), the `permission` verdict (`allow`/`deny`), inbound verdict regex; sender-gating prerequisite (gate on sender id, not room) since relay grants approval authority. |

**Estimate: 6 notes** — concept ×1 (note 1), procedure ×5 (notes 2–6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (8,240 words). New `cc_` notes: 6. New `term_dictionary` notes: 0 (Pattern B — **Channel** term owned by note 1).
- Est. total digest words: ~3,550 (avg ~590/note). Code blocks: notes 4–6 carry verbatim TypeScript/JSON/bash; each kept ≤6 (see Density Re-Assessment).
- **Building Block Distribution**: concept ×1 (note 1) · procedure ×5 (notes 2,3,4,5,6). No model/argument/empirical_observation in this sub-plan (the "how channels compare" table is folded into the concept note 1, framed as the definitional contrast, not a standalone argument note).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_channels_overview` (7 term notes)
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — A channel IS an MCP server; the note defines a channel as an MCP server that pushes events into the session, so MCP is the substrate the whole concept is built on.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents a Claude Code feature (channels) and how it compares to other Claude Code surfaces (web sessions, Slack, Remote Control), so the product term is the host this feature plugs into.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — A two-way channel exposes a reply tool Claude calls to send messages back; the note frames the chat-bridge behavior as Claude invoking a tool, the function-calling mechanism.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note describes the harness receiving pushed events into its already-running session and reacting via the agentic loop; channels extend what the harness's loop can be triggered by beyond user prompts.
- [WebSocket](../../term_dictionary/term_websocket.md) — The note's push-vs-poll distinction (events arrive in the open session rather than being polled) is the same server-initiated, bidirectional delivery model WebSocket exemplifies, clarifying why a channel is "two-way."
- [Agent Client Protocol (ACP)](../../term_dictionary/term_acp_agent_client_protocol.md) — ACP's tool-permission-relay and session primitives parallel the channel contract's reply + permission-relay shapes; the term grounds the agent-host messaging pattern channels implement over MCP.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Channels exist so Claude can keep working autonomously and stay reachable while you are away from the terminal — the unattended, long-running operating mode this term defines.

### 2. `cc_channels_setup` (6 term notes)
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — Each supported channel is an MCP server installed as a plugin; the setup steps configure credentials and start the MCP subprocess via `--channels`, so MCP is the runtime being installed.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Every step in the note runs inside Claude Code (`/plugin install`, `--channels`, `/telegram:configure`), so the product term anchors the CLI/slash-command surface the procedure operates on.
- [Slack](../../term_dictionary/term_slack.md) — Telegram/Discord/iMessage are chat platforms wired to Claude exactly as Slack is, and the page positions channels alongside the Slack integration; the term grounds the team-chat-platform category these channels join.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The pairing + allowlist step (and iMessage self-chat bypass) is the progressive trust gate that decides which senders may push messages; the note's "lock down access" step is graduated-trust enforcement.
- [Safelist](../../term_dictionary/term_safelist.md) — Each channel maintains a sender allowlist bootstrapped by pairing (`/telegram:access policy allowlist`); the term is the allowlist/whitelist exception mechanism the setup configures.
- [Voice Call (Substrate)](../../term_dictionary/term_voice_call.md) — The iMessage channel reads the Messages DB and sends via AppleScript — a platform-substrate bridge directly analogous to the voice-call substrate that hides telephony plumbing from the agent.

### 3. `cc_channels_security_and_enterprise_controls` (7 term notes)
- [Safelist](../../term_dictionary/term_safelist.md) — The note's core is the per-channel sender allowlist: only added IDs can push, everyone else is silently dropped — the allowlist/whitelist 100%-pass exception mechanism this term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — Channels default to blocked (Team/Enterprise) and senders default to dropped unless explicitly allowed; the note's posture is exactly deny-by-default, earning access through the allowlist rather than a blocklist.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Availability is gated in layers (org `channelsEnabled` → `allowedChannelPlugins` → per-session `--channels` opt-in → sender allowlist), the progressive-trust escalation this term describes.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The note clarifies that being in `.mcp.json` isn't enough to push messages — the MCP server must also be named in `--channels` — so it refines how MCP-server registration interacts with channel enablement.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `channelsEnabled` and `allowedChannelPlugins` are Claude Code managed settings configured in the claude.ai admin console; the product term anchors the enterprise-control surface.
- [Prompt-Injection Defense (DM Policy)](../../term_dictionary/term_dm_policy.md) — The allowlist exists because an ungated channel lets anyone put text in front of Claude; the term's DM-trust-boundary policy is the same untrusted-inbound-message threat model the controls mitigate.
- [Blocklist](../../term_dictionary/term_blocklist.md) — The note explicitly contrasts the allowlist approach with a permissive blocklist model (an empty `allowedChannelPlugins` array blocks all); the term grounds the blocklist alternative the design rejects.

### 4. `cc_build_a_channel` (7 term notes)
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The note builds an MCP server from the `@modelcontextprotocol/sdk`: the `Server` constructor, stdio transport, and capability declaration are all standard MCP, so MCP is the protocol the channel is implemented against.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — Channel notifications (`notifications/claude/channel`) and the `<channel>` payload are JSON-RPC notification methods carried over MCP; the term defines the transport-agnostic named-method/notification envelope the contract uses.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code spawns the channel server as a stdio subprocess, reads `.mcp.json`, and registers the notification listener from the `claude/channel` capability; the product term is the host that drives the contract.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note explains how pushed `<channel>` events feed into Claude's reasoning and how the `instructions` string steers tool routing; the event-to-action flow is the function-calling loop the channel feeds.
- [WebSocket](../../term_dictionary/term_websocket.md) — The webhook receiver listens on a local HTTP port and (in the two-way variant) streams outbound over SSE; the term grounds the persistent, server-push delivery model contrasted with request-response polling here.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note frames the channel server as a bridge between external systems and the harness's running session, injecting events into the loop the harness manages.
- [Agent Client Protocol (ACP)](../../term_dictionary/term_acp_agent_client_protocol.md) — ACP re-uses MCP JSON shapes and adds agent-host primitives like session messaging; the channel contract is a parallel MCP-extension pattern, making ACP a directly comparable agent-host wire protocol.

### 5. `cc_channel_reply_tool` (6 term notes)
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note registers a `reply` MCP tool with an `inputSchema` (chat_id, text) that Claude calls to send messages back — the canonical function-calling/tool-use pattern (schema + structured invocation).
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The reply tool is a standard MCP tool registered via `ListToolsRequestSchema`/`CallToolRequestSchema` handlers and discovered through the `tools: {}` capability; nothing about it is channel-specific, so MCP defines the tool layer.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code discovers the tool at startup and shows the user the tool call + "sent" confirmation while the reply lands on the other platform; the product term anchors the discovery + terminal-display behavior.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — Tool discovery and invocation are JSON-RPC request/response pairs over MCP (ListTools → tool list, CallTool → result); the term defines the request/response envelope the reply tool rides on.
- [WebSocket](../../term_dictionary/term_websocket.md) — The note streams outbound replies over Server-Sent Events so `curl -N` can watch them live; the term grounds the persistent server-push stream the local test harness uses.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The `instructions` string is added to Claude's system prompt to tell it when/how to route replies; this is the harness wiring tool-use guidance into the model, the harness's context-management role.

### 6. `cc_channel_permission_relay` (7 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Relay lets a remote user approve or deny tool use (Bash/Write/Edit) in the session; the note's whole subject is extending the trust-escalation approval gate to another device while keeping the local dialog live.
- [Deny-First](../../term_dictionary/term_deny_first.md) — A verdict with a wrong/unissued `request_id` is dropped silently and the dialog stays open — unrecognized approvals fail closed; the relay applies allow only on an exact ID match, the fail-safe-defaults posture.
- [Agent Client Protocol (ACP)](../../term_dictionary/term_acp_agent_client_protocol.md) — ACP explicitly adds a tool-permission-relay primitive on top of MCP JSON shapes; the channel `claude/channel/permission` capability is the same coding-UX permission-relay pattern, making ACP the closest protocol analog.
- [Prompt-Injection Defense (DM Policy)](../../term_dictionary/term_dm_policy.md) — The note mandates declaring the relay capability ONLY if the channel authenticates the sender, because anyone who can reply could approve tool use; the DM-trust-boundary policy is exactly this untrusted-inbound gating requirement.
- [Safelist](../../term_dictionary/term_safelist.md) — Relay verdicts are accepted only from senders on the channel's allowlist (the note's "gate on sender first" check precedes the verdict branch); the allowlist exception mechanism is the prerequisite control.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The relay uses MCP notification handlers (`setNotificationHandler`) for `permission_request` and emits the `permission` verdict via `mcp.notification()`; MCP is the transport carrying the relay loop's messages.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code (not Claude) generates the request ID, opens the local dialog, forwards the prompt to the channel, and applies whichever verdict arrives first; the product term is the orchestrator of the four-step relay loop.

## Section Coverage Map

```
channels.md
├── intro (what a channel is, two-way, always-on) ─ → note 1 (cc_channels_overview)
├── Supported channels (Telegram/Discord/iMessage) → note 2 (cc_channels_setup)
│   └── plugin install / marketplace mechanics ──── → linked out (B09A plugins / B09B marketplaces)
├── Quickstart (fakechat localhost demo) ────────── → note 2
│   ├── --dangerously-skip-permissions / -p mode ── → linked out (B05A permission-modes); summarized in note 2
├── Security (sender allowlist, pairing, --channels gate) → note 3 (cc_channels_security_and_enterprise_controls)
├── Enterprise controls (channelsEnabled / allowedChannelPlugins) → note 3
│   ├── Enable channels for your organization ───── → note 3
│   ├── Restrict which channel plugins can run ──── → note 3
│   └── managed-settings layering generally ─────── → linked out (B03A settings / B14B server-managed-settings)
├── Research preview (version gate, dev flag) ───── → note 1
├── How channels compare (web/Slack/MCP/Remote) ── → note 1 (→ B12B web/remote, B13A Slack, B08A mcp, B11 scheduled-tasks)
└── Next steps (cards) ──────────────────────────── → notes 1/4 (links)
channels-reference.md
├── intro (one-way vs two-way contract) ─────────── → note 1
├── Overview (architecture, stdio subprocess) ───── → note 1 / note 4 (architecture detail)
├── What you need (MCP SDK, runtime, 3 obligations) → note 4 (cc_build_a_channel)
├── Example: build a webhook receiver ───────────── → note 4
│   └── .mcp.json registration ──────────────────── → note 4 (→ B08A mcp config detail)
├── Test during the research preview (dev flag) ── → note 4
├── Server options (constructor field table) ────── → note 4
├── Notification format (content/meta, <channel>) ─ → note 4
├── Expose a reply tool ─────────────────────────── → note 5 (cc_channel_reply_tool)
├── Gate inbound messages (sender check) ────────── → note 6 (cc_channel_permission_relay) [prereq] + note 3 (concept)
├── Relay permission prompts ────────────────────── → note 6
│   ├── How relay works (4-step loop) ───────────── → note 6
│   ├── Permission request fields ───────────────── → note 6
│   ├── Add relay to a chat bridge ──────────────── → note 6
│   └── Full example ────────────────────────────── → note 6
├── Package as a plugin ─────────────────────────── → note 4 (→ B09A plugins / B09B marketplaces)
└── See also (cards) ────────────────────────────── → notes 1/4/5/6 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| channels.md (2.7Kw, 6 H2, 13 code, mixed concept+procedure) | notes 1,2,3 + link-outs | distinct BBs: the channel concept + comparison + preview (concept, note 1) vs per-platform install/quickstart steps (procedure, note 2) vs security/enterprise config (procedure, note 3); plugin/permission-mode/managed-settings owned by B09/B05/B03/B14 |
| channels-reference.md (5.5Kw >2500, 8 H2, 17 code) | notes 4,5,6 (+ overview→note 1) | exceeds word AND code caps; three distinct buildable artifacts — base one-way webhook server (note 4), two-way reply tool (note 5), permission-relay extension (note 6) — each a self-contained walkthrough; keeping whole would put 17 code blocks in one note (>6 cap) |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_channels_overview | concept | 600 | 1 | ✅ (comparison table + 1 `<channel>` example block) |
| 2 | cc_channels_setup | procedure | 600 | 5 | ✅ (`/plugin install`, `/x:configure`, `claude --channels`, `/x:access`, fakechat — collapsed per-platform; ≤6) |
| 3 | cc_channels_security_and_enterprise_controls | procedure | 500 | 2 | ✅ (settings table + 1 `allowedChannelPlugins` JSON + pairing steps) |
| 4 | cc_build_a_channel | procedure | 700 | 5 | ✅ (mkdir/bun-add, webhook.ts base, .mcp.json, dev-flag start, curl POST + `<channel>` output) |
| 5 | cc_channel_reply_tool | procedure | 450 | 4 | ✅ (capability snippet, ListTools/CallTool handlers, instructions, SSE note) |
| 6 | cc_channel_permission_relay | procedure | 700 | 6 | ✅ AT CAP (capability, permission-request fields table, request handler, verdict regex, gate-on-sender, 3-terminal curl test) — if a draft needs a 7th block, fold the field table to prose; do NOT inline the page's "Full example" mega-block (link to source) |

Notes 4–6 carry the most code; each is held ≤6 blocks by summarizing the page's two `expandable` "Full
webhook.ts" mega-listings as prose + a source link rather than transcribing them (G3 + grounding both
satisfied — the canonical contract snippets are kept verbatim, the redundant full assemblies are linked).
No note exceeds caps; every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_channels_overview cc_channels_setup cc_channels_security_and_enterprise_controls cc_build_a_channel cc_channel_reply_tool cc_channel_permission_relay"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (6 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination; code blocks verbatim | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met (note 6 at the 6-code cap); every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 6 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 6 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (in-degree ≥1, verified) | DB confirms inbound in-degree ≥1 per note after inlinks applied | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 6 rows** under a "Channels" cluster + increments the BB-distribution counts
(concept +1, procedure +5).

## Undigested Terms Plan (Step 4e)

b08b creates **no new `term_dictionary` notes** — the channel vocabulary is covered by a b08b `cc_` concept
note, an existing substantive term note (link), or a home sub-plan (Pattern B). Dedup checked across
**both** `term_dictionary/` AND `resources/documentation/` (the `claude_code/` folder does not yet exist;
no `cc_channel*` collision):

| Term (page) | Disposition |
|---|---|
| Channel | note 1 `cc_channels_overview` (doc concept — B08B owns it per master) |
| MCP server / stdio transport | link `term_mcp` (exists); protocol detail owned by B08A `mcp.md` |
| JSON-RPC notification | link `term_json_rpc` (exists) |
| Plugin / marketplace / `/plugin install` | owned by B09A `plugins.md` / B09B `plugin-marketplaces.md` — captured there |
| Permission mode / `--dangerously-skip-permissions` | owned by B05A `permission-modes.md` — linked, not recreated |
| Managed settings (`channelsEnabled`, `allowedChannelPlugins`) | folded into note 3 as channel-specific config; general managed-settings model owned by B03A `settings.md` / B14B |
| Sender allowlist / pairing | link `term_safelist` + `term_graduated_trust` (exist); described in notes 2/3/6 |
| Prompt injection | link `term_dm_policy` (exists; the vault's prompt-injection/DM-trust term); corpus-wide "Prompt injection" term owned by B16 `security-guidance.md` per master |
| Reply tool / notification format / permission relay | folded into notes 4/5/6 as channel-contract procedure detail (not standalone terms) |
| Non-interactive mode (`-p`) | mentioned in note 2; owned by B11 `headless.md` — linked, not recreated |
| Webhook / SSE | link `term_websocket` (closest existing networking term); SSE described inline (no dedicated term, not a vault-wide vocabulary gap) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages scanning emphasis/tables/captions/code
comments for newly-surfaced terms. Candidates examined: "permission relay", "notification format",
"sender allowlist", "research preview", "development flag" — all are channel-contract feature names
covered inline by notes 1/3/4/6, not cross-cutting vocabulary needing a `term_dictionary` capture. No
non-glossary term with no doc-page home AND no existing note surfaced. **0 new B08B `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B08B authors zero term notes, so there are
no slugs to audit. The collision check that matters here (do the channel concepts duplicate existing
`term_dm_policy`, `term_websocket`, `term_deny_first`, `term_blocklist`, `term_acp`, `term_slack`,
`term_function_calling`, `term_agent_harness`, `term_autonomous_coding_agents`, `term_claude_code`,
`term_voice_call` all exist → linked, not recreated. The `Channel` doc-concept (note 1) has no existing
`cc_*` or term collision (no `claude_code/` folder, no `*channel*` doc note in scope).

## Term-Note Authoring Requirements

**N/A for b08b** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- **Code blocks verbatim** — notes 4/5/6 transcribe the canonical contract snippets exactly from
  `channels-reference.md`; the two `expandable` "Full webhook.ts" mega-listings are summarized + linked
  to source rather than transcribed (keeps each note ≤6 code blocks). One BB per note. Each note ≤400
  lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island, G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_mcp.md` | notes 1, 4 | MCP term → a concrete MCP-server-as-channel pattern + the build-your-own contract |
| `term_dictionary/term_acp.md` | notes 1, 6 | ACP term (agent-host permission relay) → the channel concept + its permission-relay contract |
| `term_dictionary/term_safelist.md` | note 3 | allowlist term → channel sender-allowlist security controls |
| `term_dictionary/term_graduated_trust.md` | note 6 | trust-escalation term → remote permission-relay approval |
| `term_dictionary/term_claude_code.md` | note 1 | product term → the channels feature overview |
| `term_dictionary/term_websocket.md` | notes 4, 5 | persistent-push/SSE term → the webhook server + SSE reply stream |

## Follow-up Recommendations

- After the 6 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and verify
  DB in-degree ≥1 per note (G7/G8); queue the 6 rows for `entry_claude_code_docs.md` under a "Channels"
  cluster; `/tessellum-check-broken-links`. Cross-link note 1 to the eventual B12B Remote Control, B13A
  Slack, and B11 scheduled-tasks notes once those sub-plans execute (the "how channels compare" siblings).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13** — see Review Sign-Off below (READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B08B, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read in full from `inbox/claude_code_docs/`; measured words
  channels 2,696 · channels-reference 5,544 = 8,240, matching the master's 8,240 figure. channels-reference
  (5,544w, 17 code) exceeds both the word AND code caps → forced the 3-way split (notes 4/5/6); channels
  (2,696w) split by BB (notes 1/2/3). No >1.5× under-estimate beyond those documented splits.
- **Notes**: 6 (concept 1, procedure 5) — matches master estimate. Splits documented in Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note**
  standard — 6–7 term notes per note (14 distinct `term_dictionary/` terms), each with a per-link
  false positives discarded (e.g. `term_safelist` kept because the allowlist concept genuinely matches the
  channel sender allowlist; BRP-only matches like `term_reversibility_weighted_risk` dropped). **All 14
- **Step 2d new-term scan**: candidates examined (permission relay, notification format, sender allowlist,
  research preview, dev flag) — all channel-contract feature names covered inline; **0 new B08B term captures**.
- **Dedup (Step 2b across term_dictionary AND documentation/)**: `claude_code/` folder does not exist yet;
  no `cc_channel*` collision; 15 candidate terms all confirmed existing → linked, not recreated.
- **Sections present**: Scope, Content Strategy, Source Pages (measured), Planned Notes (LOCKED), Summary
  Statistics & BB Distribution, Per-Note Related Notes Mapping (LOCKED), Section Coverage Map, Split
  Decisions, Density Re-Assessment (LOCKED), Validation Scripts, Per-Phase Validation Gate (G1–G8), Entry
  Point Decision, Undigested Terms Plan, Term-Note Authoring Requirements, Pacing Rules, Inlinks,
  Follow-up Recommendations, Pipeline Status, Augmentation Report, Review Sign-Off.
- **28-item checklist**: PASS (term-note items N/A — B08B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented, then reviewed (below) — set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present incl G7/G8 Discoverability (single phase). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B08B contributes 6 rows under a Channels cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 6 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | Inherits master Format Definition verbatim — YAML field order, `## Overview` opener, source-mirrored H2s, `## Related Notes` indexed links, `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | channels-reference (5.5Kw / 17 code) split into 3; note 6 sits AT the 6-code cap with a documented fold-to-prose escape valve; notes 1–5 comfortably under. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Re-measured: channels 2,696 + channels-reference 5,544 = 8,240 = master 8,240. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B08B authors 0 term notes; Undigested Terms Plan routes channel vocabulary (Channel→note 1; MCP/JSON-RPC/allowlist/etc.→existing terms; plugin/permission-mode/managed-settings→home sub-plans); Authoring Requirements inherited. |
| CP9 | Discoverability / inlinks executed-plan present (G7/G8) | ✅ PASS | Inlinks table maps ≥1 inbound link per note from outside `claude_code/` (term_mcp, term_acp, term_safelist, term_graduated_trust, term_claude_code, term_websocket → all 6 notes); in-degree ≥1 verified at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
