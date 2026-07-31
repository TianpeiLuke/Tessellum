---
title: Sub-Plan pf03 — OpenClaw Docs: Platforms (macOS — Peekaboo, Permissions, Remote, Signing, Skills, Voice Overlay)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["platforms/mac/peekaboo", "platforms/mac/permissions", "platforms/mac/remote", "platforms/mac/signing", "platforms/mac/skills", "platforms/mac/voice-overlay"]
---

# Sub-Plan pf03: Platforms

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → bold footer), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master.

## Scope

The 6 macOS-app platform pages covering the native OpenClaw.app integration surface on macOS: the
PeekabooBridge UI-automation broker (`peekaboo`), TCC permission persistence and recovery
(`permissions`), the remote-gateway control flow over SSH/direct WebSocket (`remote`), debug-build code
signing (`signing`), the gateway-backed Skills settings UI (`skills`), and the wake-word/push-to-talk
voice overlay lifecycle (`voice-overlay`). Priority **P2 (Phase B)** per master — these are
platform-integration/operational pages that reference the gateway, security, voice, and skills vocabulary
defined in Phase A. The code-side counterparts (`repo_openclaw_apps`, `repo_openclaw_security`,
`repo_openclaw_extensions_voice_speech`, `repo_openclaw_gateway`, `repo_openclaw_skills`) are LINKED, not
recreated.

**Source**: OpenClaw docs, 6 pages, 3,267 measured words. **Planned: 6 notes (1 per page).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| peekaboo | /platforms/mac/peekaboo | 533 | 1 | 8 | 0 | concept |
| permissions | /platforms/mac/permissions | 486 | 1 | 5 | 0 | procedure |
| remote | /platforms/mac/remote | 1,060 | 3 | 11 | 0 | procedure |
| signing | /platforms/mac/signing | 464 | 1 | 4 | 1 | procedure |
| skills | /platforms/mac/skills | 225 | 0 | 5 | 0 | concept |
| voice-overlay | /platforms/mac/voice-overlay | 499 | 1 | 6 | 0 | concept |

Total measured: 3,267 words, 7 code fences, 39 H2, 1 H3.

## Content Strategy

- **Prioritize**: the operationally load-bearing pages — `permissions` (TCC stability + recovery is the
  prerequisite for every other macOS capability), `remote` (the full remote-gateway control flow:
  modes, transports, app setup, security), and `signing` (signing is what makes permissions persist).
  `peekaboo` is the conceptual hub explaining the three distinct desktop-control paths (PeekabooBridge
  host vs Codex Computer Use vs direct `cua-driver` MCP).
- **Split**: none. All 6 pages are well under the 2,500-word cap (largest is `remote` at 1,060w) and
  each is single-BB; 1 note per page keeps each note atomic. `peekaboo` mixes a concept body (path
  comparison) with a short "Enable the bridge" procedure, but at 533w the concept frame dominates and the
  enable steps are a sub-procedure inside the concept note — no split warranted.
- **Link-out (not duplicated)**: macOS permission/Accessibility internals (TCC) → cross-reference
  `term_posix_permissions` / `term_access_control`, not redefined; voice-wake runtime details →
  link `term_voice_wake` and sibling `platforms/mac/voicewake` (pf04); gateway auth modes / remote
  access / Tailscale / security → link gateway-series notes (gw04–gw06, planned) + `term_tls` /
  `term_ssh` / `term_tunneling`; Skills tool details → `term_skills` + `tools/skills` (to07, planned);
  Codex Computer Use + `cua-driver` MCP → `term_mcp` (the MCP-server framing), not redefined here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_platforms_mac_peekaboo.md` | concept | peekaboo.md: What this is (and is not), Relationship to Computer Use, Enable the bridge, Client discovery order, Security and permissions, Snapshot behavior, Troubleshooting | 500 | OpenClaw.app as a permission-aware PeekabooBridge host for macOS UI automation: what the broker is/is not, how it relates to the three desktop-control paths (PeekabooBridge host vs Codex Computer Use vs direct cua-driver MCP), enabling the local UNIX socket, client discovery order, code-signature/TeamID allowlist security, and snapshot behavior. |
| 2 | `oc_platforms_mac_permissions.md` | procedure | permissions.md: Requirements for stable permissions, Accessibility grants for Node and CLI runtimes, Recovery checklist when prompts disappear, Files and folders permissions (Desktop/Documents/Downloads) | 480 | Keeping macOS TCC permission grants stable: why grants are fragile (signature/bundle-id/path identity), why to avoid granting Accessibility to a generic `node` runtime, the tccutil recovery checklist when prompts disappear, and Desktop/Documents/Downloads file-access gating with the workspace workaround. |
| 3 | `oc_platforms_mac_remote.md` | procedure | remote.md: Modes, Remote transports, Prereqs on the remote host, macOS app setup, Web Chat, Permissions, Security notes, WhatsApp login flow (remote), Troubleshooting, Notification sounds | 720 | Using the macOS app as a full remote control for an OpenClaw gateway on another host: local vs remote-over-SSH vs remote-direct modes, SSH-tunnel vs direct ws/wss transports, remote-host prereqs, `openclaw-mac configure-remote` setup, Web Chat over the forwarded port, remote TCC permissions, loopback/auth security, remote WhatsApp QR login, and troubleshooting (exit 127, stale TLS pins). |
| 4 | `oc_platforms_mac_signing.md` | procedure | signing.md: (intro on package-mac-app.sh), Usage, Ad-hoc Signing Note, Build metadata for About, Why | 470 | Signing macOS debug builds via `package-mac-app.sh`: the stable debug bundle id, `codesign-mac-app.sh` invocation, real-cert vs ad-hoc signing (`SIGN_IDENTITY`/`ALLOW_ADHOC_SIGNING`), Hardened-Runtime handling for ad-hoc, Team ID audit, build-metadata stamping for the About pane, and why stable signature + bundle id + path preserve TCC grants. |
| 5 | `oc_platforms_mac_skills.md` | concept | skills.md: Data source, Install actions, Env/API keys, Remote mode | 320 | How the macOS app surfaces OpenClaw skills via the gateway (it does not parse skills locally): `skills.status` eligibility + missing requirements, `skills.install` installer selection (brew/uv/node-manager/go/download, install-policy gating), env/API-key storage in `openclaw.json`, and remote-mode install behavior on the gateway host. |
| 6 | `oc_platforms_mac_voice_overlay.md` | concept | voice-overlay.md: Current intent, Implemented (Dec 9, 2025), Next steps, Debugging checklist, Migration steps | 480 | The macOS voice-overlay lifecycle when wake-word and push-to-talk overlap: how a push-to-talk hotkey adopts an existing wake-word overlay's text, per-capture session tokens that drop stale callbacks, the planned VoiceSessionCoordinator/VoiceSession/publisher actor model, the unified send-or-dismiss path with cooldown, and the `voicewake` log-stream debugging checklist. |

## Section Coverage Map

```
peekaboo.md (8 H2)
├── What this is (and is not) ───────────────────── → note 1 (oc_platforms_mac_peekaboo)
├── Relationship to Computer Use ────────────────── → note 1 (3 desktop-control paths)
├── Enable the bridge ───────────────────────────── → note 1 (sub-procedure)
├── Client discovery order ──────────────────────── → note 1
├── Security and permissions ────────────────────── → note 1 (links note 2)
├── Snapshot behavior (automation) ──────────────── → note 1
├── Troubleshooting ─────────────────────────────── → note 1
└── Related ─────────────────────────────────────── → note 1 References / Related Notes
permissions.md (5 H2)
├── Requirements for stable permissions ─────────── → note 2 (oc_platforms_mac_permissions)
├── Accessibility grants for Node and CLI runtimes  → note 2
├── Recovery checklist when prompts disappear ───── → note 2 (tccutil)
├── Files and folders permissions (Desktop/…) ───── → note 2
└── Related ─────────────────────────────────────── → note 2 References / Related Notes
remote.md (11 H2)
├── (intro) ─────────────────────────────────────── → note 3 (oc_platforms_mac_remote) Overview
├── Modes ───────────────────────────────────────── → note 3
├── Remote transports ───────────────────────────── → note 3 (SSH tunnel vs direct ws/wss)
├── Prereqs on the remote host ──────────────────── → note 3
├── macOS app setup ─────────────────────────────── → note 3 (configure-remote)
├── Web Chat ────────────────────────────────────── → note 3
├── Permissions ─────────────────────────────────── → note 3 (links note 2)
├── Security notes ──────────────────────────────── → note 3
├── WhatsApp login flow (remote) ────────────────── → note 3
├── Troubleshooting ─────────────────────────────── → note 3
├── Notification sounds ─────────────────────────── → note 3
└── Related ─────────────────────────────────────── → note 3 References / Related Notes
signing.md (4 H2 / 1 H3)
├── (intro on package-mac-app.sh) ───────────────── → note 4 (oc_platforms_mac_signing) Overview
├── Usage ───────────────────────────────────────── → note 4
│   └── Ad-hoc Signing Note (H3) ────────────────── → note 4
├── Build metadata for About ────────────────────── → note 4
├── Why ─────────────────────────────────────────── → note 4 (links note 2)
└── Related ─────────────────────────────────────── → note 4 References / Related Notes
skills.md (5 H2)
├── (intro) ─────────────────────────────────────── → note 5 (oc_platforms_mac_skills) Overview
├── Data source ─────────────────────────────────── → note 5 (skills.status)
├── Install actions ─────────────────────────────── → note 5 (skills.install)
├── Env/API keys ────────────────────────────────── → note 5
├── Remote mode ─────────────────────────────────── → note 5 (links note 3)
└── Related ─────────────────────────────────────── → note 5 References / Related Notes
voice-overlay.md (6 H2)
├── (intro) ─────────────────────────────────────── → note 6 (oc_platforms_mac_voice_overlay) Overview
├── Current intent ──────────────────────────────── → note 6
├── Implemented (Dec 9, 2025) ───────────────────── → note 6 (session tokens, PTT adoption)
├── Next steps ──────────────────────────────────── → note 6 (Coordinator/Session/publisher model)
├── Debugging checklist ─────────────────────────── → note 6 (log stream)
├── Migration steps (suggested) ─────────────────── → note 6
└── Related ─────────────────────────────────────── → note 6 References / Related Notes
```
No orphaned sections. Every H2/H3 across all 6 pages maps to a planned note. "Related" sections become
each note's `## References` (external doc-site cross-links) + `## Related Notes` (vault cross-refs). Linked
(not duplicated): voicewake runtime (pf04, planned), Skills tool (to07, planned), gateway security/remote/
Tailscale (gw04–gw06, planned), macOS-app overview page (pf04, planned), Talk mode (nd02, planned).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 6 pages ≤ 1,060 words (largest = `remote`), each single-BB; no page exceeds the 2,500-word or 6-code-block cap, so 1 note per page is correct. `peekaboo.md` contains a short "Enable the bridge" procedure inside a concept body, but at 533w the concept (path comparison + broker role) is the dominant BB and the enable steps are an inline sub-procedure — no mixed-BB split needed. |

## Summary Statistics & Building Block Distribution

- Source pages: 6 (3,267 words). New `oc_` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×3** (notes 1 peekaboo, 5 skills, 6 voice-overlay) · **procedure ×3**
  (notes 2 permissions, 3 remote, 4 signing).
- Est. digest words ~2,970 (avg ~495/note; range 320–720). 7 source code fences distribute one-to-one
  across notes (peekaboo 1 / permissions 1 / remote 3 / signing 1 / skills 0 / voice-overlay 1); every
  note stays ≤6 code blocks. All notes ≤400 lines / ≤2,500 words.
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note meets the raised floors **≥8
  sibling `oc_*` (this series). Per-note totals: peekaboo 10t/11s/11d · permissions 8t/10s/11d · remote
  12t/12s/12d · signing 10t/10s/11d · skills 10t/11s/11d · voice_overlay 10t/12s/11d. Exact locked
  mapping with per-link relevance statements is in the "## Per-Note Related Notes Mapping" section.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read; no
> note_id='<id>'"`) on 2026-06-21 — terms 75/77 candidates resolved (`term_state_machine`,
> `term_session` MISS → dropped), 84/84 docs, 88/88 snippets, 10/10 repos, both analysis notes, and
> other openclaw sub-plans) and `entry_openclaw_docs` do not exist yet → marked **(planned)** and counted
> Relative paths from `resources/documentation/openclaw/oc_X.md`: term →
> `../../term_dictionary/term_Y.md`; sibling oc_ → `oc_Y.md`; other doc → `../<folder>/<file>.md`
> (`../claude_code/cc_Y.md`, `../hermes_agent/hermes_Y.md`, `../pi/pi_Y.md`, `../band/band_Y.md`); snippet →
> `../../code_snippets/snippet_Y.md`; repo → `../../../areas/code_repos/repo_Y.md`; analysis →
> `../../analysis_thoughts/analysis_Y.md`; entry → `../../../0_entry_points/entry_Y.md`.

### oc_platforms_mac_peekaboo (10t · 11s · 12d)

**Terms**
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool-server standard; relevance: the two non-bridge desktop-control paths (Codex `computer-use` MCP server, direct `cua-driver mcp`) are registered as normal MCP servers.
- [Computer Use](../../term_dictionary/term_code_execution_tool.md) — agent tool that issues sandboxed system actions; relevance: PeekabooBridge primitives (screenshots, clicks, menus, Dock) are the macOS computer-use surface OpenClaw brokers.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic GUI/web driving; relevance: Peekaboo is the broad macOS UI-automation surface, the desktop analog of browser automation.
- [IPC](../../term_dictionary/term_ipc.md) — inter-process communication; relevance: the bridge runs a local UNIX-socket server so the `peekaboo` client and host app communicate over IPC.
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — persistent socket transport for host/client control; relevance: the bridge is a local socket server with a client discovery order and overridable `PEEKABOO_BRIDGE_SOCKET` path.
- [Access Control](../../term_dictionary/term_access_control.md) — identity-gated permission enforcement; relevance: the bridge validates caller code signatures against a TeamID allowlist (Peekaboo + OpenClaw TeamIDs).
- [Sandbox](../../term_dictionary/term_sandbox.md) — bounded execution context; relevance: the broker is permission-aware, mediating automation within the app's TCC-granted boundary rather than granting raw GUI access.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed dev agents; relevance: Codex-mode agents own native desktop-control during Codex turns, one of the three paths peekaboo contrasts.
- [ACP](../../term_dictionary/term_acp_agent_client_protocol.md) — Agent Client Protocol runtime control surface; relevance: frames how an external agent runtime drives the macOS app's automation primitives.
- [a2ui](../../term_dictionary/term_a2ui.md) — agent-to-UI rendering/control surface; relevance: positions Peekaboo's broker-host UI-automation model against agent-driven UI control.

**Docs**
- [cc_computer_use](../claude_code/cc_computer_use.md) — Claude Code computer-use feature; relevance: closest analog to the Codex Computer Use path peekaboo contrasts (screenshots/clicks via a tool surface).
- [cc_computer_use_safety](../claude_code/cc_computer_use_safety.md) — computer-use safety model; relevance: parallels peekaboo's signature/TeamID-allowlist + timeout safety posture for desktop control.
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — macOS computer-use in the Hermes agent; relevance: same OS, same TCC-gated screenshot/click primitives as the PeekabooBridge host.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — browser automation backend setup; relevance: the GUI-automation-broker pattern (host owns permissions, client drives) mirrors peekaboo's bridge model.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — supervised automation backend lifecycle; relevance: parallels the bridge host lifecycle (start/stop socket server, fall back to other hosts).
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome automation surface; relevance: another desktop-control path comparison for the "which automation surface to use" decision.
- [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — registering MCP servers; relevance: the `cua-driver mcp` path registers as a normal MCP server exactly as this doc describes.
- [hermes_use_mcp_guide](../hermes_agent/hermes_use_mcp_guide.md) — using MCP servers in an agent; relevance: explains the MCP-server framing for the non-bridge desktop-control paths.
- [band_mcp_overview](../band/band_mcp_overview.md) — MCP architecture overview; relevance: foundation for the three-path comparison's MCP-server option.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — selecting among automation backends; relevance: directly parallels peekaboo's "which desktop-control surface to use" decision across the bridge / Codex computer-use / cua-driver paths.
- `oc_platforms_macos` (pf04, planned, this series) — macOS app overview; relevance: parent page that the bridge host setting lives under.
- `oc_platforms_mac_permissions` (planned, this series) — the Accessibility-for-`node` warning peekaboo links directly.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: hosts the PeekabooBridge socket server and owns the TCC permissions it reuses.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: implements the caller-signature validation + TeamID allowlist the bridge enforces.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled extensions; relevance: home of the `codex` plugin that prepares Codex app-server / `computer-use` MCP.

**Snippets**
- [snippet_hermes_agent_tools_computer_use_schema](../../code_snippets/snippet_hermes_agent_tools_computer_use_schema.md) — computer-use tool schema; relevance: the action vocabulary (click/screenshot/type) the bridge brokers.
- [snippet_hermes_agent_tools_computer_use_tool](../../code_snippets/snippet_hermes_agent_tools_computer_use_tool.md) — computer-use tool impl; relevance: how a desktop-control tool dispatches primitives, mirroring bridge calls.
- [snippet_hermes_agent_tools_computer_use_cua_backend](../../code_snippets/snippet_hermes_agent_tools_computer_use_cua_backend.md) — CUA driver backend; relevance: the direct `cua-driver mcp` path peekaboo describes, at code level.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: snapshot capture is a core Peekaboo primitive (in-memory, short TTL).
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM/element addressing; relevance: parallels Peekaboo's element/window-index automation workflow.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — automation-host lifecycle; relevance: start/stop/fallback host management like the bridge host.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback MCP HTTP server; relevance: the local-socket/loopback broker pattern, same as the bridge UNIX socket.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — registering agent tools; relevance: how the CUA driver gets exposed to an agent runtime as a tool.
- [snippet_hermes_agent_tools_mcp_client](../../code_snippets/snippet_hermes_agent_tools_mcp_client.md) — MCP client connection; relevance: the registration mechanics for the `cua-driver mcp` / Codex computer-use server.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: how desktop-control tools are catalogued for a runtime, framing the three-path choice.
- [snippet_brp_agent_tools_screenshot](../../code_snippets/snippet_brp_agent_tools_screenshot.md) — screenshot tool; relevance: another implementation of the screenshot primitive the bridge exposes.

### oc_platforms_mac_permissions (8t · 10s · 12d)

**Terms**
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS-level file/identity access bits; relevance: macOS gates Desktop/Documents/Downloads by process context, the file-access half of this page.
- [Access Control](../../term_dictionary/term_access_control.md) — identity-gated permission model; relevance: TCC ties each grant to code signature + bundle id + path identity — the page's central thesis.
- [Sandbox](../../term_dictionary/term_sandbox.md) — bounded per-process permission context; relevance: each process context (Terminal, LaunchAgent, SSH) needs its own grant.
- [POSIX](../../term_dictionary/term_posix.md) — POSIX process/runtime model; relevance: the `node`/CLI runtime identity that TCC sees is a POSIX process.
- [Node.js](../../term_dictionary/term_node_js.md) — the Node runtime; relevance: granting Accessibility to a shared `node` binary leaks GUI automation to every package it launches — the page's key warning.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: npm/nvm/pnpm workflows route through one shared `node` executable that can inherit the grant.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: a Homebrew-installed `node` is exactly the shared-executable case the page warns against.
- [IPC](../../term_dictionary/term_ipc.md) — inter-process communication / process context; relevance: background/SSH/LaunchAgent processes performing file ops each have a distinct TCC identity.

**Docs**
- [hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md) — macOS computer-use permissions; relevance: same TCC Accessibility/Screen-Recording grant prerequisites this page stabilizes.
- [cc_computer_use](../claude_code/cc_computer_use.md) — computer-use feature; relevance: desktop control requires the very macOS permissions whose persistence this page covers.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission model; relevance: distinguishes sandboxing from OS permission grants, the conceptual frame for TCC fragility.
- [cc_sandbox_limitations_and_troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — permission/sandbox troubleshooting; relevance: parallels the recovery-checklist when grants/prompts disappear.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — filesystem isolation; relevance: the Desktop/Documents/Downloads file-access gating is OS-level filesystem isolation.
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation setup; relevance: documents the Microphone/Speech-Recognition TCC grants also listed among required approvals.
- [pi_security_model](../pi/pi_security_model.md) — agent security/permission model; relevance: the least-privilege rationale for granting to a signed helper, not a generic runtime.
- [pi_containerization](../pi/pi_containerization.md) — process isolation; relevance: the "grant per process context" principle in containerized/isolated runtimes.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: stable install path + signed binary are the install-side prerequisites for grant persistence.
- [cc_desktop_permission_modes](../claude_code/cc_desktop_permission_modes.md) — desktop-app permission grant modes; relevance: the per-process / per-context permission-grant model is exactly the TCC grant-per-context problem (Terminal vs LaunchAgent vs SSH) this page stabilizes.
- `oc_platforms_mac_signing` (planned, this series) — signing is the prerequisite for stable grants (reciprocal); relevance: the page links signing as the "why grants stick".
- `oc_platforms_mac_peekaboo` (planned, this series) — the Accessibility-for-`node` warning referenced here.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the signed macOS app; relevance: the bundle-id/signature identity that should own grants instead of `node`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: the permission/identity model and code-signature policy underlying TCC stability.

**Snippets**
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — filesystem exec policy; relevance: code-side gating of file operations that the OS folder-permissions complement.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime exec audit; relevance: identifies which runtime/process context performs an operation, the TCC-identity question.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list for dangerous tools; relevance: the "don't grant broad GUI automation to a shared runtime" principle in code.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: constrains what the `node` runtime may do, mitigating the shared-executable grant risk.
- [snippet_openclaw_cli_root_guard](../../code_snippets/snippet_openclaw_cli_root_guard.md) — root/privilege guard; relevance: refuses over-broad privilege, the same caution as not granting Accessibility to `node`.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — code-exec sandbox; relevance: per-process execution boundary that determines which identity TCC sees.
- [snippet_hermes_agent_core_file_safety](../../code_snippets/snippet_hermes_agent_core_file_safety.md) — file-safety checks; relevance: guards file reads against contexts lacking folder grants (the Desktop/Documents/Downloads gate).
- [snippet_hermes_agent_core_context_references_path_safety](../../code_snippets/snippet_hermes_agent_core_context_references_path_safety.md) — path-safety; relevance: the workspace-relocation workaround (`~/.openclaw/workspace`) is path-scoped file access.
- [snippet_hermes_agent_tools_file_tools](../../code_snippets/snippet_hermes_agent_tools_file_tools.md) — file tool operations; relevance: the file-read/list operations that hang without the right folder grant.

### oc_platforms_mac_remote (12t · 12s · 12d)

**Terms**
- [SSH](../../term_dictionary/term_ssh.md) — Secure Shell; relevance: the default remote transport uses `ssh -N -L` with key auth and `~/.ssh/known_hosts` host-key checking.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote SSH dev/execution; relevance: OpenClaw commands execute on the remote host over the SSH connection the app opens.
- [Tunneling](../../term_dictionary/term_tunneling.md) — port-forward/tunnel networking; relevance: the SSH tunnel forwards the gateway port to localhost (`ws://127.0.0.1:18789`); also the Tailscale framing.
- [TLS](../../term_dictionary/term_tls.md) — Transport Layer Security; relevance: `wss://` direct mode and the stale TLS leaf-pin / `gateway.remote.tlsFingerprint` handling after cert rotation.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — certificate pinning; relevance: the app detects stale legacy TLS leaf pins and clears them when macOS trusts the rotated cert.
- [WebSocket](../../term_dictionary/term_websocket.md) — ws/wss transport; relevance: the gateway control port (default 18789) and Web Chat ride the WebSocket transport.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: a public HTTPS reverse proxy is a direct-mode option, and `trusted-proxy` auth is an identity-aware reverse proxy.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS LAN discovery; relevance: same-LAN gateways advertise Bonjour and auto-fill the SSH-target field from the discovered list.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: non-loopback binds require valid gateway auth — token, password, or `trusted-proxy` mode.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: "Test remote" runs `openclaw status --json`; health checks reuse the same remote config.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS permission grants; relevance: the remote host needs the same TCC approvals (Automation, Accessibility, Screen Recording, Mic, Speech) as local.
- [VPN](../../term_dictionary/term_vpn.md) — virtual private network overlay; relevance: Tailscale/Tailnet is the recommended off-LAN reachability layer for stable remote IPs.

**Docs**
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — auth flow over SSH; relevance: same SSH-tunnel-to-remote-host pattern with credential handling.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote desktop backend; relevance: directly analogous app-as-remote-control-of-a-backend architecture.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote control of an agent host; relevance: the same "drive a host on another machine" control flow.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network TLS/access; relevance: the wss/TLS and trusted-network access considerations of direct mode.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: reverse-proxy and gateway-URL configuration for direct (ws/wss) transport.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket control overview; relevance: the WebSocket control-port transport Web Chat and CLI share.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: token/password gateway auth for remote access, matching the security-notes section.
- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — API server auth setup; relevance: loopback-bind + auth-required posture for exposing a gateway.
- [hermes_messaging_whatsapp_baileys](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — WhatsApp/Baileys login; relevance: the remote WhatsApp QR login flow (`openclaw channels login`) and Baileys session.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth/network error triage; relevance: parallels the troubleshooting (exit 127, health-probe failed, stuck WS) section.
- `oc_platforms_mac_permissions` (planned, this series) — remote host needs the same TCC grants (linked from Permissions section).
- `oc_gateway_remote` (gw05, planned, this series) — the gateway-side remote access this page's app-side flow connects to.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: the remote OpenClaw gateway being controlled (loopback bind, WS control port, auth modes).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: the remote-control client that manages the SSH tunnel / direct connection.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels subsystem; relevance: the remote WhatsApp/Baileys login flow runs through channels.

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: the direct (ws/wss) connection through a reverse proxy / gateway URL.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection; relevance: the WebSocket control transport the app opens to the gateway.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: token / password / trusted-proxy gateway auth modes the security notes require.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — gateway TLS pinning; relevance: the stale-leaf-pin detection + `tlsFingerprint` behavior for `wss://*.ts.net`.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity over TLS; relevance: client-side TLS identity for direct wss connections.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — gateway pairing; relevance: the paired/disconnected device state the troubleshooting section diagnoses.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — server HTTP/WS listen; relevance: loopback vs non-loopback bind the security notes discuss.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: gateway-side auth gating of RPC calls over the remote connection.
- [snippet_hermes_agent_tools_environments_ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — SSH environment; relevance: SSH transport with key auth and host-key handling, mirroring the tunnel setup.
- [snippet_hermes_agent_cli_web_websocket](../../code_snippets/snippet_hermes_agent_cli_web_websocket.md) — web WS client; relevance: Web Chat over the forwarded WebSocket control port.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: the gateway token (`OPENCLAW_GATEWAY_TOKEN`) passed at configure-remote.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session; relevance: node-host service + `node.list`/`node.describe` permission-state advertisement.

### oc_platforms_mac_signing (10t · 10s · 12d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — identity-gated permissions; relevance: TCC grants are bound to the code signature — the page's central "why signing matters".
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS-level grant identity; relevance: grants are tied to bundle id + signature + fixed path (`dist/OpenClaw.app`).
- [Node.js](../../term_dictionary/term_node_js.md) — Node runtime; relevance: packaging defaults to Node 24 (Node 22 LTS supported) for TS and Control-UI builds.
- [Sandbox](../../term_dictionary/term_sandbox.md) — runtime isolation; relevance: ad-hoc signing disables Hardened Runtime (`--options runtime`) to load embedded frameworks like Sparkle.
- [Signature Classes](../../term_dictionary/term_signature_classes.md) — code-signature categories; relevance: distinguishes real Developer ID / Apple Development certs from ad-hoc (`-`) signatures.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: `SIGN_IDENTITY` is the signing identity (Developer ID cert) that authenticates the bundle.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: build-toolchain context for the packaging script's environment.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: the `pnpm`/Node build the packager runs for TS and Control-UI.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — pinned-identity trust; relevance: stable signature identity is the macOS-side analog of pinning — the OS recognizes the same bundle across rebuilds.
- [IAM](../../term_dictionary/term_iam.md) — identity-and-access management; relevance: the Team ID audit enforces a single signing identity across all Mach-O in the bundle.

**Docs**
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — install verification; relevance: signature/build verification parallels the Team ID audit and About-pane build metadata.
- [cc_install_failures_reference](../claude_code/cc_install_failures_reference.md) — install-failure triage; relevance: signing/identity failures (mismatched Team ID, ad-hoc) surface as the same class of install problems.
- [hermes_desktop_app](../hermes_agent/hermes_desktop_app.md) — desktop app build/distribution; relevance: same macOS-app packaging-and-signing concern for a coding-agent desktop app.
- [cc_install](../claude_code/cc_install.md) — install procedure; relevance: stable install path + signed binary are the persistence prerequisites this page documents.
- [cc_update_and_release_channels](../claude_code/cc_update_and_release_channels.md) — release channels; relevance: debug/release channel stamping (`#if DEBUG`, build metadata for the About pane).
- [hermes_profile_distributions](../hermes_agent/hermes_profile_distributions.md) — distribution profiles; relevance: signed-build distribution model for desktop agents.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS/trust; relevance: trusted timestamps (`CODESIGN_TIMESTAMP=auto`) for Developer ID signatures.
- [pi_packages](../pi/pi_packages.md) — packaging/build; relevance: the build-and-package pipeline that produces the signed bundle.
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update/uninstall; relevance: rebuild-and-reinstall keeping a stable bundle id so grants persist.
- [hermes_profile_distribution_model](../hermes_agent/hermes_profile_distribution_model.md) — signed-build distribution model; relevance: the identity-stable signed-bundle distribution this page's signing/Team-ID audit produces, viewed from the distribution side.
- `oc_platforms_mac_permissions` (planned, this series) — the "why" — signing preserves TCC grants (reciprocal, linked from page).
- `oc_platforms_mac_dev_setup` (pf02, planned, this series) — the build setup that invokes `package-mac-app.sh`.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app bundle; relevance: the bundle that `package-mac-app.sh` builds and `codesign-mac-app.sh` signs.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: the Team ID audit / signature-policy enforcement.

**Snippets**
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: Info.plist / launch metadata generation analogous to the bundle-id + build-metadata stamping.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — restart handoff; relevance: stable bundle id/path across restarts so the OS treats rebuilds as the same app.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile cache / respawn; relevance: the build-and-respawn pipeline the packager drives (TS build, Control UI).
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — bootstrap shell script; relevance: a packaging/bootstrap script structure parallel to `package-mac-app.sh`.
- [snippet_hermes_agent_acp_bootstrap_ps1](../../code_snippets/snippet_hermes_agent_acp_bootstrap_ps1.md) — bootstrap PowerShell; relevance: cross-platform build/sign bootstrap counterpart.
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — macOS app menu/sessions; relevance: macOS app code surface (About pane shows the stamped build/git metadata).
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — signature verification; relevance: code-signature/integrity-verification pattern analogous to the Team ID audit.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: bundle/manifest metadata (build timestamp, git commit) stamping.
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — macOS app native code; relevance: a macOS-app Swift component inside the bundle subject to the Team ID audit / Hardened Runtime.

### oc_platforms_mac_skills (10t · 11s · 12d)

**Terms**
- [Skills](../../term_dictionary/term_skills.md) — the OpenClaw skill abstraction; relevance: the macOS app surfaces skills via the gateway (`skills.status`/`skills.install`).
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — SKILL.md metadata; relevance: requirements derive from `metadata.openclaw.requires`; install options from `metadata.openclaw.install`.
- [Skills Hub](../../term_dictionary/term_skills_hub.md) — skill registry/distribution; relevance: the catalog the gateway resolves eligibility and installers against.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin metadata schema; relevance: the `metadata.openclaw.*` namespace shared with plugin manifests.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin/skill authoring SDK; relevance: how `requires`/`install` declarations are authored and consumed.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registered-capability catalog; relevance: skills are gateway-registered, eligibility-gated capabilities.
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: a node-manager installer option (incl. `yarn` labels) the gateway can pick.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: Homebrew is the first preferred installer when `preferBrew` is on and `brew` exists.
- [Access Control](../../term_dictionary/term_access_control.md) — policy-gated permissions; relevance: operator-owned `security.installPolicy` can block gateway-backed skill installs.
- [Authentication](../../term_dictionary/term_authentication.md) — credential storage; relevance: per-skill `apiKey`/`env` stored under `skills.entries.<skillKey>` in `openclaw.json`.

**Docs**
- [hermes_skills_system](../hermes_agent/hermes_skills_system.md) — skills system; relevance: the same gateway-managed skill model (status, eligibility, install).
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub; relevance: gateway-host install of skills, matching remote-mode install behavior.
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — using skills; relevance: end-user surface for enabling/configuring skills like the macOS settings UI.
- [hermes_creating_skill_format](../hermes_agent/hermes_creating_skill_format.md) — SKILL.md format; relevance: the `metadata.openclaw.requires`/`install` frontmatter this page reads.
- [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — plugin user config/env; relevance: storing per-skill `apiKey`/`env` configuration, like `skills.entries`.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — manifest schema; relevance: the manifest-driven requirements/install-options model.
- [cc_plugin_install_hints](../claude_code/cc_plugin_install_hints.md) — install hints; relevance: installer-preference selection (brew/uv/node/go/download) analog.
- [band_mcp_ai_assistant_setup](../band/band_mcp_ai_assistant_setup.md) — assistant/tool setup; relevance: API-key/env entry storage for gateway-managed capabilities.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — plugin system; relevance: the install-policy gating and plugin/skill lifecycle on the gateway host.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin/install policy settings; relevance: operator-owned policy that blocks installs, directly analogous to `security.installPolicy` gating gateway-backed skill installs.
- `oc_tools_skills` (to07, planned, this series) — the Skills tool itself this UI surfaces.
- `oc_platforms_mac_remote` (planned, this series) — remote-mode install runs on the gateway host (linked from Remote mode section).

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: the skills the gateway exposes via `skills.status`/`skills.install`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: serves the `skills.*` RPCs and runs installers on the host.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: the Skills settings UI that calls these gateway RPCs.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: the `metadata.openclaw.requires`/`install` SKILL.md schema this page reads.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skills install CLI; relevance: the installer selection + run-on-host behavior of `skills.install`.
- [snippet_hermes_agent_tools_skills_hub_install](../../code_snippets/snippet_hermes_agent_tools_skills_hub_install.md) — skills-hub install; relevance: gateway-host installer execution from the hub catalog.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills-hub registry; relevance: the catalog backing `skills.status` eligibility + missing-requirements.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validation; relevance: eligibility/requirements checking like `skills.status` reports.
- [snippet_hermes_agent_tools_skills_invoke](../../code_snippets/snippet_hermes_agent_tools_skills_invoke.md) — skill invoke; relevance: how a registered skill is invoked once installed/enabled.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills guard/policy; relevance: install-policy/dangerous-code gating analogous to `security.installPolicy`.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — SKILL.md frontmatter parse; relevance: parsing the `metadata.openclaw.*` requirements/install metadata.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package/manifest contract for installable capabilities.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: install-policy/allowlist blocking for bundled skills the page mentions.
- [snippet_hermes_agent_skills_index_cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — skills index cache; relevance: the gateway's skill index that `skills.status` returns.

### oc_platforms_mac_voice_overlay (10t · 12s · 12d)

**Terms**
- [Push-to-Talk](../../term_dictionary/term_pushtotalk.md) — hold-to-record voice input; relevance: PTT adopts an existing wake overlay's text and sends immediately on release — the page's core scenario.
- [Voice Wake](../../term_dictionary/term_voice_wake.md) — wake-word activation; relevance: wake-word auto-sends on silence; the overlay it raises is what PTT adopts.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — voice interaction mode; relevance: the overlay is the voice-mode UI surface coordinating wake-word and PTT capture.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: partial/final transcript events drive overlay text, dropped when the session token mismatches.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming transcripts; relevance: PTT waits up to 1.5s for a final transcript before falling back to current text.
- [Chime](../../term_dictionary/term_chime.md) — audio cue; relevance: send/overlay chime logging in `voicewake.chime`; `performSend` plays the send chime once.
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice-agent runtime; relevance: broader voice-agent context the overlay session model sits within.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — voice agent; relevance: the conversational voice surface the overlay feeds captured speech to.
- [Access Control](../../term_dictionary/term_access_control.md) — TCC grant model; relevance: Microphone + Speech-Recognition permissions gate voice capture.
- [IPC](../../term_dictionary/term_ipc.md) — actor/publisher messaging; relevance: the planned VoiceSessionCoordinator/VoiceSession/VoiceSessionPublisher actor model passes token-tagged messages.

**Docs**
- [cc_voice_dictation](../claude_code/cc_voice_dictation.md) — voice dictation; relevance: the closest analog — push-to-talk dictation overlay with start/stop and transcript handling.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — voice mode; relevance: wake-word + voice-mode lifecycle in a sibling coding agent.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — using voice mode; relevance: end-user wake-word/PTT behavior the overlay implements.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT transcription; relevance: partial/final transcript events and the 1.5s final-wait the overlay coordinates.
- [hermes_voice_gateway_discord_vc](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice gateway; relevance: voice-session/capture lifecycle and audio routing parallels.
- [cc_keybindings_action_reference](../claude_code/cc_keybindings_action_reference.md) — keybinding actions; relevance: the push-to-talk hotkey binding that triggers `beginPushToTalk`.
- [cc_interactive_mode_keyboard_shortcuts](../claude_code/cc_interactive_mode_keyboard_shortcuts.md) — keyboard shortcuts; relevance: hold-hotkey interaction model for push-to-talk.
- [cc_input_modes_and_editing](../claude_code/cc_input_modes_and_editing.md) — input modes/editing; relevance: the overlay's display/editing/sending modes and send-or-dismiss path.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS/audio; relevance: the chime/audio-cue side of the send path.
- [cc_keybindings_customization](../claude_code/cc_keybindings_customization.md) — customizing keybindings; relevance: configuring the hold-hotkey that triggers `beginPushToTalk` — the customizable PTT binding this overlay reacts to.
- `oc_platforms_mac_voicewake` (pf04, planned, this series) — the wake-word runtime this overlay sits atop (linked from page).
- `oc_nodes_talk` (nd02, planned, this series) — Talk mode (linked from page).

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: the STT/voice subsystem feeding transcripts to the overlay.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the macOS app; relevance: hosts the SwiftUI overlay, coordinator, and PTT hotkey handling.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: voice-wake tracking / trigger-phrase forwarding on the gateway.

**Snippets**
- [snippet_openclaw_macos_pushtotalk_overlay](../../code_snippets/snippet_openclaw_macos_pushtotalk_overlay.md) — PTT overlay; relevance: the exact overlay-adoption + send-or-dismiss code this page specifies.
- [snippet_openclaw_macos_pushtotalk_nsevent](../../code_snippets/snippet_openclaw_macos_pushtotalk_nsevent.md) — PTT NSEvent hotkey; relevance: the push-to-talk hotkey capture that begins/ends a PTT session.
- [snippet_openclaw_macos_voice_wake_trigger](../../code_snippets/snippet_openclaw_macos_voice_wake_trigger.md) — voice-wake trigger; relevance: the wake-word path that raises the overlay PTT adopts.
- [snippet_openclaw_macos_voice_wake_state](../../code_snippets/snippet_openclaw_macos_voice_wake_state.md) — voice-wake state machine; relevance: the session-state model the VoiceSession/coordinator formalizes (tokens, cooldown).
- [snippet_openclaw_macos_voice_wake_audio](../../code_snippets/snippet_openclaw_macos_voice_wake_audio.md) — voice-wake audio capture; relevance: per-capture audio session that carries the session token.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — gateway voice-wake tracking; relevance: trigger-phrase forwarding in remote mode (no separate forwarder).
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: partial/final transcript events the overlay consumes.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: voice-capture session lifecycle in a sibling agent.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: streaming-transcript handling and final-wait behavior.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the STT pipeline producing the transcripts the overlay binds to.
- [snippet_openclaw_macos_menu_sessions_control](../../code_snippets/snippet_openclaw_macos_menu_sessions_control.md) — macOS sessions control; relevance: the single-active-session ownership model the coordinator enforces.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk transcription relay; relevance: relaying transcripts in remote/Talk mode the overlay forwards to.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| PeekabooBridge / `peekaboo` CLI | OpenClaw-specific UI-automation broker → digested as concept content in `oc_platforms_mac_peekaboo` (note 1); NOT a `term_dictionary` capture. |
| Codex Computer Use / `cua-driver mcp` | OpenClaw/Codex desktop-control path → described in note 1; link existing `term_mcp` (the MCP-server framing). No new term. |
| TCC (Transparency, Consent, and Control) | macOS OS concept → described in `oc_platforms_mac_permissions` (note 2); link `term_posix_permissions` / `term_access_control`. No new term. |
| `tccutil` / Accessibility grant | macOS tooling/concept → described in note 2; no reusable cross-cutting vault term beyond `term_access_control`. No new term. |
| SSH tunnel / port-forward / loopback | networking concepts → link existing `term_ssh` + `term_tunneling`; described as config in `oc_platforms_mac_remote` (note 3). No new term. |
| ws/wss / WebSocket control port | link existing `term_websocket` + `term_websocket_framing`; config in note 3. No new term. |
| Tailscale / Tailscale Serve / Bonjour | link existing `term_tunneling` (Tailscale) + `term_bonjour_discovery`; config in note 3. (`term_tailscale` does not exist; gateway series gw06 owns any deeper Tailscale doc — link there, not a new term.) No new term. |
| `trusted-proxy` auth / identity-aware reverse proxy | link existing `term_reverse_proxy` + `term_authentication`; config in note 3. No new term. |
| code signing / Developer ID / ad-hoc / Hardened Runtime / Team ID | macOS packaging concepts → digested as procedure in `oc_platforms_mac_signing` (note 4); link `term_access_control` + `term_posix_permissions`. No new term. |
| `skills.status` / `skills.install` / install policy | OpenClaw RPC + skills vocabulary → digested in `oc_platforms_mac_skills` (note 5); link existing `term_skills` + `term_tool_registry` + `term_plugin_sdk`. No new term. |
| VoiceSessionCoordinator / wake-word / push-to-talk / overlay lifecycle | OpenClaw voice-runtime vocabulary → digested in `oc_platforms_mac_voice_overlay` (note 6); link existing `term_voice_wake` + `term_voice_mode` + `term_speech_to_text`. No new term. |

**Expected new `term_dictionary` captures: 0.** All vocabulary on these 6 pages is either (a) OpenClaw-/
macOS-app-specific (digested into the home `oc_*` doc note) or (b) covered by an existing `term_dictionary`
note that is LINKED, not redefined. No genuinely cross-cutting, vault-reusable term lacks an existing note
or a doc-page home, so no new-term candidate is proposed. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms.
Requirement inherited from master: should augment surface a genuinely cross-cutting, vault-reusable term
with no existing note AND no doc-page home, it is captured via `/tessellum-capture-term-note`, added to the
best-fit `acronym_glossary_*.md` (likely the agentic/LLM-dev glossary), and never inlined in an `oc_*` note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). All gates must pass before commit.

| Gate | Name | Check |
|------|------|-------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` — YAML field order, required `## Overview` / `## Related Notes`, bold `**Source**`/`**Last Updated**`/`**Status**` footer, single `building_block`. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/platforms/mac/<page>.md` — no fabricated commands/flags; config snippets reproduced verbatim. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | Raised floors per note: ≥8 relevance-selected `term_dictionary` links + ≥10 `code_snippets` + ≥10 docs (existing + planned sibling `oc_*`), PLUS relevant `repo_openclaw*`; each with a relevance statement; all existing targets resolve (per "## Per-Note Related Notes Mapping"). |
| G5 | Ghost-reference | Detect + redirect any link whose target note does not exist (sibling planned notes excepted but flagged). |
| G6 | Broken-link | `/tessellum-fix-broken-links` — 0 broken relative paths after reindex. |
| G7 | Discoverability (out) | Each note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 | Verify `note_links` shows in-degree ≥1 per new note (anti-island) before commit. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_platforms_mac_peekaboo oc_platforms_mac_permissions oc_platforms_mac_remote oc_platforms_mac_signing oc_platforms_mac_skills oc_platforms_mac_voice_overlay"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density: words (frontmatter-stripped) ≤2500, code fences ≤6, lines ≤400
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # G4 sibling-series link presence (oc_ prefix among Related Notes)
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n NO SIBLING oc_ LINK"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6/G8 after incremental reindex
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  echo "$n in_degree=${indeg:-MISSING}"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_platforms_mac_peekaboo | concept | 500 | 1 | ✅ |
| 2 | oc_platforms_mac_permissions | procedure | 480 | 1 | ✅ |
| 3 | oc_platforms_mac_remote | procedure | 720 | 3 | ✅ |
| 4 | oc_platforms_mac_signing | procedure | 470 | 1 | ✅ |
| 5 | oc_platforms_mac_skills | concept | 320 | 0 | ✅ |
| 6 | oc_platforms_mac_voice_overlay | concept | 480 | 1 | ✅ |

No note approaches any cap (≤2,500w / ≤6 code / ≤400 lines). The most code-dense source (`remote`, 3
fences) and the longest source (`remote`, 1,060w → ~720w note) both stay comfortably within limits; no
split required.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, since the corpus
exceeds 30 notes) under a **"Platforms — macOS"** cluster (shared with pf01/pf02/pf04). Each new note
receives its entry-point back-link at finalization, satisfying G7/G8. No standalone entry point for this
6-note sub-plan (master hub owns navigation). Parent-hub wiring (W2: `entry_gen_ai_dev`,

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; all sources below confirmed present):

- `entry_openclaw_docs.md` (planned hub, master pre-step) → **all 6 notes** (primary G7/G8 satisfier).
- `repo_openclaw_apps.md` → notes 1, 2, 3, 4, 5, 6 (the macOS app implements every page's surface).
- `repo_openclaw_security.md` → notes 1, 2, 4 (signature/TeamID/permission policy).
- `repo_openclaw_gateway.md` → notes 3, 5, 6 (remote control, gateway-backed skills, voice-wake tracking).
- `repo_openclaw_skills.md` → note 5 (skills subsystem).
- `repo_openclaw_extensions_voice_speech.md` → note 6 (voice/speech extension).
- `repo_openclaw_extensions.md` → note 1 (bundled `codex` plugin path).
- `repo_openclaw_channels.md` → note 3 (remote WhatsApp/Baileys login).
- `term_voice_wake.md` → note 6; `term_skills.md` → note 5; `term_posix_permissions.md` → notes 2, 4;
  `term_ssh.md` / `term_tunneling.md` → note 3; `term_mcp.md` → note 1.
- `analysis_openclaw_vs_claude_kiro_skills.md` → note 5;

sibling links (note 2 ↔ note 4 signing/permissions; note 3 → note 2; note 5 → note 3; note 1 → note 2)
are added within the series at execution.

## Pacing Rules (inherited from master)

One execution phase (6 notes). Re-read each source page before drafting; reproduce config/CLI snippets
verbatim (G2). One `building_block` per note. Cap dynamic-workflow fan-out at ~30 agents/run; reindex
incrementally before the gate sweep; verify `note_links` + 0 broken links + in-degree ≥1 before commit.
Commit+push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of pf03 (6 macOS platform notes) to the raised cross-reference floors
**≥8 terms · ≥10 snippets · ≥10 docs per note**, relevance-selected from a fresh re-read of all 6 source

**What was locked:**
- Replaced the candidate "## Candidate Cross-References" with "## Per-Note Related Notes Mapping (LOCKED)":
  per-note grouped **Terms / Docs / Repos / Snippets** lists, every link with a what-it-is + per-note
  relevance statement.
- Updated Summary Statistics cross-ref line + G4 gate to the raised floors.

**Per-note counts (terms / snippets / docs / repos; floors ≥8 / ≥10 / ≥10):**

| Note | Terms | Snippets | Docs | Repos | Floors met |
|---|---:|---:|---:|---:|---|
| oc_platforms_mac_peekaboo | 10 | 11 | 11 (9 existing + 2 planned) | 3 | ✅ |
| oc_platforms_mac_permissions | 8 | 10 | 11 (9 existing + 2 planned) | 2 | ✅ |
| oc_platforms_mac_remote | 12 | 12 | 12 (10 existing + 2 planned) | 3 | ✅ |
| oc_platforms_mac_signing | 10 | 10 | 11 (9 existing + 2 planned) | 2 | ✅ |
| oc_platforms_mac_skills | 10 | 11 | 11 (9 existing + 2 planned) | 3 | ✅ |
| oc_platforms_mac_voice_overlay | 10 | 12 | 11 (9 existing + 2 planned) | 3 | ✅ |

`oc_*` docs are clearly marked and never counted toward the existing-doc minimum. ALL snippets are existing

**DB-verification result (2026-06-21):** terms 75/77 candidates resolved · docs 84/84 · snippets 88/88 ·
(planned W1 master pre-step, as expected). The two MISS terms — `term_state_machine`, `term_session` —
were the candidates the draft itself flagged as unconfirmed; both DROPPED (every note still clears ≥8 terms
without them; voice_overlay's state/session concepts are carried by `snippet_openclaw_macos_voice_wake_state`
+ `term_voice_mode` + `term_pushtotalk`).

**New-term candidates:** none. Consistent with the master's corpus-wide design decision (OpenClaw vocabulary
is digested as `oc_*` documentation concept notes by its home sub-plan, not as new `term_dictionary`
entries) and pf03's Undigested Terms Plan (Expected new term captures: 0). The re-read surfaced no
genuinely cross-cutting, vault-reusable term lacking both an existing note and a doc-page home. All
page-specific vocabulary (PeekabooBridge, `cua-driver mcp`, TCC/`tccutil`, `trusted-proxy`, Hardened
Runtime/Team ID, `skills.status`/`skills.install`, VoiceSessionCoordinator/PTT) is either OpenClaw/macOS-
specific (digested into its home `oc_*` note) or covered by an existing linked term. Step 2d re-scan
confirms 0 new terms; best-fit glossary (had any surfaced) would be the agentic/LLM-dev glossary.

**Issues / watch-items for execution:** (1) `entry_openclaw_docs.md` must be CREATED at master pre-step W1
before pf03 commits (G7/G8 inbound-link satisfier); until then the 6 notes' primary outside-folder inbound
link comes from `repo_openclaw_apps` + the term/analysis inlinks listed in "## Inlinks". (2) Sibling `oc_*`
links (pf02/pf04/gw05/to07/nd02) are planned, not yet created — they resolve as G5-excepted planned
targets; the executor must not treat them as ghosts but should flag them for back-fill when those sub-plans
land. (3) The Codex plugin reference path (pl02/pl07) was dropped from the locked peekaboo mapping in favor

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table present per phase (G1–G6, G8, G9) | **PASS** | "## Per-Phase Validation Gate (G1–G9)" — single execution phase lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7 Discoverability-out, G8 In-degree≥1. G5+G6 present; G8 anti-island present. |
| CP3 | Entry point specified / inherited | **PASS** | "## Entry Point Decision" inherits `entry_openclaw_docs.md` (CREATED at master W1 since corpus >30 notes); pf03 contributes 6 rows under "Platforms — macOS"; parent-hub wiring at master. `entry_openclaw_docs` correctly NOT-yet-present (DB-confirmed) and flagged W1 pre-step. |
| CP4 | Plan size (≤30 or split) | **PASS** | 6 notes ≤30; single phase. |
| CP5 | Note format aligned + DERIVED | **PASS** | Format inherited verbatim from master, derived from the existing `claude_code/`(`cc_*`)+`pi/`(`pi_*`) doc corpora in the same `resources/documentation/` dir: `## Overview` opener, `## Related Notes`, bold `**Source**`/`**Last Updated**`/`**Status**` footer, single `building_block`, forbidden-field list. Relative-path forms validated against the live `documentation/` tree. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: largest note remote ~720w / 3 code (vs caps 2500w/6cb/400L); none borderline. peekaboo concept+enable-sub-procedure correctly kept single-BB (533w, concept dominant). |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 2026-06-21: peekaboo 494w/1cb, permissions 437w/1cb, remote 1036w/3cb, signing 440w/1cb, skills 197w/0cb, voice-overlay 479w/1cb — all within 0.85–1.0× of plan estimates (well inside the 0.7–1.3 band); no under-estimation. |
| CP8 | Undigested Terms Plan + Authoring Requirements + slug/collision audit | **PASS** | "## Undigested Terms Plan" present (11 rows, all disposition = link existing / digest in-note, 0 new captures); "## Term-Note Authoring Requirements" present (N/A — 0 new terms; inherited mandate for any surfaced term). 0 `term_*` slugs to create ⇒ specificity/collision audit vacuously satisfied; collision audit generalized to the 6 doc notes — none duplicates an existing term/doc note (peekaboo links `term_mcp` not a `cc_mcp`-style dup; voice_overlay links `term_voice_wake`/`term_voice_mode` rather than recreating). |
| CP8f | Slug/collision audit (doc-notes too) | **PASS** | All 6 planned `oc_platforms_mac_*` slugs are page-specific and collision-checked: no existing `documentation/` or `term_dictionary/` note covers any of the 6 macOS-app pages (DB grep `entry_openclaw_docs`/`oc_*` confirms openclaw doc folder has no platform notes yet). No too-general slugs. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | "## Inlinks" maps every new note to ≥1 outside-folder inbound source (all 6 ← `entry_openclaw_docs` W1 + `repo_openclaw_apps`; plus repo/term/analysis inlinks), and G8 In-degree≥1 is a gate in the phase table marked as verified before commit (EXECUTED phase, not "recommended"). |

**RESULT: 9/9 (10/10 incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

DB-verify command used during authoring:
