---
title: Sub-Plan to02 — OpenClaw Docs: Tools (Browser Troubleshooting, Browser Login, WSL2 CDP, BTW, Code Execution, Creating Skills, Diffs)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/browser-linux-troubleshooting", "tools/browser-login", "tools/browser-wsl2-windows-remote-cdp-troubleshooting", "tools/btw", "tools/code-execution", "tools/creating-skills", "tools/diffs"]
---

# Sub-Plan to02: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML frontmatter + `## Overview` + source-mirrored body + `## Related Notes` + `## References` + bold footer), dedup (3-way across term_dictionary / documentation / `repo_openclaw*`), 9-GATE validation, cross-references, and entry-point wiring (W1–W5) are ALL inherited from the master — not restated here.

## Scope

The 7 tool pages covering **browser control / troubleshooting** (Linux CDP startup, manual login, WSL2↔Windows remote CDP), the **`/btw` ephemeral side-question tool**, the **`code_execution` sandboxed remote-Python tool**, **creating skills** (authoring + publishing agent skills), and the **`diffs` read-only diff viewer plugin tool**. These are the agent-facing capability/operations pages of the Tools section. **Priority: P2 (Phase B — features/integration)**; they reference the concepts/runtime vocabulary defined in Phase A and the existing `repo_openclaw*` code corpus, the `term_skills`/`term_browser_automation`/`term_cdp`/`term_subagent`/`term_code_execution_tool` term notes, and the `cc_*` sibling docs for browser/skill/exec/diff tools.

**Source**: OpenClaw docs, 7 pages, **6,953 measured words** (mirror `inbox/openclaw_docs/tools/`). **Planned: 8 notes** (diffs.md splits 2-way; the 3 browser pages each = 1 note).

## Source Pages (Measured 2026-06-20, mirror inbox/openclaw_docs/)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| browser-linux-troubleshooting | tools/browser-linux-troubleshooting | 785 | 9 | 2 | 7 | procedure |
| browser-login | tools/browser-login | 339 | 3 | 5 | 0 | procedure |
| browser-wsl2-windows-remote-cdp-troubleshooting | tools/browser-wsl2-windows-remote-cdp-troubleshooting | 1,073 | 5 | 10 | 8 | procedure |
| btw | tools/btw | 830 | 2 | 8 | 3 | concept |
| code-execution | tools/code-execution | 698 | 4 | 5 | 0 | procedure |
| creating-skills | tools/creating-skills | 1,099 | 5 | 7 | 4 | procedure |
| diffs | tools/diffs | 2,129 | 5 | 19 | 1 | procedure + model (SPLIT) |

Totals: **6,953 words · 33 code fences · 56 H2 · 23 H3.** Code-fence counts are `grep -c '^```' / 2` per page; H1 lines in the source (`# ~/.config/...`, `# Propose a brand-new skill`, etc.) are inline shell-comment/example artifacts inside code fences, NOT real section headers, and are NOT counted as H2/H3.

## Content Strategy

- **Prioritize**: the `code_execution` setup + the `creating-skills` authoring procedure (the two reusable agent-capability how-tos), and the `diffs` tool-input/security contract (most complex, splits). The three browser pages are operational troubleshooting runbooks — kept faithful (failure text + fix commands verbatim) but each stays one focused note.
- **Split**: only **diffs.md (2,129w, 19 H2)** — splits into a usage/config **procedure** note (install/enable/modes, tool-input reference, syntax highlighting, plugin defaults, persistent viewer URL) and a viewer/security **model** note (output-details contract, collapsed sections, artifact lifecycle/storage, viewer URL+network behavior, security model, browser requirements, troubleshooting, operational guidance). Mixed-BB + nearing the 2,500w cap justifies the split (master rule: >2,500w OR mixed-BB ⇒ split). All other pages are single-note reference/runbook pages.
- **Link-out (do NOT redefine)**: `tools/browser` + `tools/browser-control` (sibling to01); `tools/plugin` + `tools/skills`/`tools/skills-config`/`tools/skill-workshop`/`tools/slash-commands`/`tools/subagents` (sibling to06/to07); `gateway/sandboxing` + `gateway/sandbox-vs-tool-policy-vs-elevated` (gw05); ClawHub publishing (cw01/cw02); `concepts/agent-workspace`/`concepts/session` (co01/co06). Existing terms (`term_browser_automation`, `term_cdp`, `term_skills`, `term_code_execution_tool`, `term_xai`, `term_sandbox`) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_browser_linux_troubleshooting.md` | procedure | browser-linux-troubleshooting.md (all: Failed-to-start-CDP problem, Root cause, Solution 1 install Chrome, Solution 2 snap Chromium attach-only, Verifying, Config reference, No-Chrome-tabs problem) | 500 | Fixing Chrome/Brave/Edge/Chromium CDP startup failures for OpenClaw browser control on Linux: root cause (snap confinement), installing system Chrome, snap Chromium attach-only mode, verification, and the "no tabs found" profile problem. |
| 2 | `oc_tools_browser_login.md` | procedure | browser-login.md (all: Manual login, Which Chrome profile is used, X/Twitter recommended flow, Sandboxing + host browser access) | 350 | Manual logins for OpenClaw browser automation: the recommended manual-login flow, which Chrome profile is used, the X/Twitter posting flow, and host-browser access under sandboxing. |
| 3 | `oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting.md` | procedure | browser-wsl2-windows-remote-cdp-troubleshooting.md (all: Choose the right mode [Option 1 raw remote CDP / Option 2 host-local Chrome MCP], Working architecture, Why confusing, Critical Control-UI rule, Validate in layers [Layers 1–5], Common misleading errors, Fast triage checklist, Practical takeaway) | 700 | Layered troubleshooting for WSL2 Gateway ↔ Windows Chrome remote CDP: choosing remote-CDP vs host-local MCP mode, the working architecture, layer-by-layer validation (Chrome serving CDP, WSL2 reachability, profile, Control UI, end-to-end), and the triage checklist. |
| 4 | `oc_tools_btw.md` | concept | btw.md (all: What it does, What it does not do, How context works, Delivery model, Surface behavior [TUI / External channels / Control UI], When to use, When not to use) | 550 | The `/btw` ("by the way") tool: ephemeral side-questions that read conversation context but are not persisted to the transcript — what it does and doesn't do, how context is supplied, the delivery model, per-surface behavior, and when (not) to use it. |
| 5 | `oc_tools_code_execution.md` | procedure | code-execution.md (all: Setup, How to use it, Errors, Limits) | 500 | The `code_execution` tool: running sandboxed remote Python analysis via xAI — setup/configuration, how the agent invokes it, the error surface, and the limits/constraints. |
| 6 | `oc_tools_creating_skills.md` | procedure | creating-skills.md (all: Create your first skill, SKILL.md reference [Required/Optional fields, `{baseDir}`], Adding conditional activation, Propose via Skill Workshop, Publishing to ClawHub, Best practices) | 650 | Authoring OpenClaw agent skills: creating a first skill, the SKILL.md frontmatter reference (required/optional fields, `{baseDir}`), conditional activation, proposing via the Skill Workshop, publishing to ClawHub, and best practices. |
| 7 | `oc_tools_diffs_usage.md` | procedure | diffs.md: Quick start, Disable built-in system guidance, Typical agent workflow, Input examples, Tool input reference, Syntax highlighting, Plugin defaults, Persistent viewer URL config | 650 | Using the `diffs` diff-viewer plugin tool: install/enable, view/file/both modes, the full tool-input reference, syntax-highlighting languages + language pack, plugin-wide defaults, and persistent viewer-URL config. |
| 8 | `oc_tools_diffs_viewer_security.md` | model | diffs.md: Output details contract, Collapsed unchanged sections, Artifact lifecycle and storage, Viewer URL and network behavior, Security model, Browser requirements for file mode, Troubleshooting, Operational guidance | 600 | The `diffs` viewer artifact + security model: the `details` output contract (viewer/file fields, mode behavior), artifact lifecycle/TTL/storage, viewer URL construction + network behavior, viewer/file-render hardening (loopback, CSP, throttling), Chromium requirements, and operational guidance. |

## Section Coverage Map

```
browser-linux-troubleshooting.md
├── Problem: "Failed to start Chrome CDP on port 18800" ─ → note 1 (oc_tools_browser_linux_troubleshooting)
│   ├── Root cause ─────────────────────────────────────── → note 1
│   ├── Solution 1: Install Google Chrome (Recommended) ── → note 1
│   ├── Solution 2: Snap Chromium Attach-Only Mode ─────── → note 1
│   ├── Verifying the Browser Works ────────────────────── → note 1
│   ├── Config reference ───────────────────────────────── → note 1
│   └── Problem: "No Chrome tabs found for profile" ────── → note 1
└── Related ───────────────────────────────────────────── → note 1 References / link-out (browser to01)
browser-login.md
├── Manual login (recommended) ────────────────────────── → note 2 (oc_tools_browser_login)
├── Which Chrome profile is used? ─────────────────────── → note 2
├── X/Twitter: recommended flow ───────────────────────── → note 2
├── Sandboxing + host browser access ──────────────────── → note 2
└── Related ───────────────────────────────────────────── → note 2 References / link-out
browser-wsl2-windows-remote-cdp-troubleshooting.md
├── Choose the right browser mode first (Option 1 / 2) ── → note 3 (oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting)
├── Working architecture ──────────────────────────────── → note 3
├── Why this setup is confusing ───────────────────────── → note 3
├── Critical rule for the Control UI ──────────────────── → note 3
├── Validate in layers (Layers 1–5) ───────────────────── → note 3
├── Common misleading errors ──────────────────────────── → note 3
├── Fast triage checklist ─────────────────────────────── → note 3
├── Practical takeaway ────────────────────────────────── → note 3
└── Related ───────────────────────────────────────────── → note 3 References / link-out
btw.md
├── What it does / What it does not do ────────────────── → note 4 (oc_tools_btw)
├── How context works ─────────────────────────────────── → note 4
├── Delivery model ────────────────────────────────────── → note 4
├── Surface behavior (TUI / External channels / Control UI) → note 4
├── When to use BTW / When not to use BTW ──────────────── → note 4
└── Related ───────────────────────────────────────────── → note 4 References / link-out
code-execution.md
├── Setup ─────────────────────────────────────────────── → note 5 (oc_tools_code_execution)
├── How to use it ─────────────────────────────────────── → note 5
├── Errors ────────────────────────────────────────────── → note 5
├── Limits ────────────────────────────────────────────── → note 5
└── Related ───────────────────────────────────────────── → note 5 References / link-out
creating-skills.md
├── Create your first skill ───────────────────────────── → note 6 (oc_tools_creating_skills)
├── SKILL.md reference (Required/Optional fields, {baseDir}) → note 6
├── Adding conditional activation ─────────────────────── → note 6
├── Propose via Skill Workshop ────────────────────────── → note 6
├── Publishing to ClawHub ─────────────────────────────── → note 6
├── Best practices ────────────────────────────────────── → note 6
└── Related ───────────────────────────────────────────── → note 6 References / link-out
diffs.md
├── (intro: inputs, outputs, system-prompt guidance) ──── → note 7 (oc_tools_diffs_usage, Overview)
├── Quick start (install / enable / pick a mode) ──────── → note 7
├── Disable built-in system guidance ──────────────────── → note 7
├── Typical agent workflow ────────────────────────────── → note 7
├── Input examples ────────────────────────────────────── → note 7
├── Tool input reference ──────────────────────────────── → note 7
├── Syntax highlighting ───────────────────────────────── → note 7
├── Plugin defaults (+ Persistent viewer URL config) ──── → note 7
├── Output details contract (Viewer/File/Compat fields, Mode behavior) → note 8 (oc_tools_diffs_viewer_security)
├── Collapsed unchanged sections ──────────────────────── → note 8
├── Artifact lifecycle and storage ────────────────────── → note 8
├── Viewer URL and network behavior ───────────────────── → note 8
├── Security model (viewer/file hardening) ────────────── → note 8
├── Browser requirements for file mode ────────────────── → note 8
├── Troubleshooting ───────────────────────────────────── → note 8
├── Operational guidance ──────────────────────────────── → note 8
└── Related ───────────────────────────────────────────── → notes 7 & 8 References / link-out
```
No orphaned sections. Each page's trailing `## Related` block maps to the note's `## References` + `## Related Notes` link-out (siblings to01/to06/to07, gateway sandboxing, ClawHub).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| diffs.md (2,129w · 19 H2 · 5 code · mixed BB) | note 7 `oc_tools_diffs_usage` (procedure) + note 8 `oc_tools_diffs_viewer_security` (model) | Nears the 2,500w cap AND mixes two BBs: a usage/config **procedure** (install→enable→modes→input→defaults) vs the viewer-artifact **model + security contract** (output-details fields, artifact lifecycle/TTL, URL/network behavior, viewer/file hardening). Master rule (>2,500w OR mixed-BB ⇒ split) + one-BB-per-note rule. Each half ≤650w, ≤4 code fences. |
| browser-linux-troubleshooting.md (785w) | note 1 only | Single focused Linux-CDP runbook (one BB, <800w). No split. |
| browser-wsl2-windows-remote-cdp-troubleshooting.md (1,073w) | note 3 only | One cohesive layered troubleshooting runbook (one BB, ~1,073w < 2,500). The 5 validation layers are one procedure, not separable atomic tasks. No split. |
| creating-skills.md (1,099w) | note 6 only | Single create→author→propose→publish procedure (one BB, ~1,099w). No split. |
| (browser-login, btw, code-execution) | notes 2, 4, 5 (1 each) | All <850w, single BB. No split. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (6,953 measured words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0** (expected).
- BB distribution: **procedure ×6** (notes 1, 2, 3, 5, 6, 7) · **concept ×1** (note 4 `oc_tools_btw`) · **model ×1** (note 8 `oc_tools_diffs_viewer_security`).
- Est. digest words **~4,500** (avg ~560/note); all notes ≤700w, ≤6 code fences — well within caps. The 33 source fences distribute across notes; the code-heaviest page (browser-linux-troubleshooting, 9 fences) → 1 note keeps only the load-bearing install/config/systemd snippets (≤6).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_tools_browser_linux_troubleshooting (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control for agents; relevance: the whole page is fixing OpenClaw's browser-control server, the browser-automation subsystem.
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: the failure is "Failed to start Chrome CDP on port 18800" — CDP is the control transport being launched.
- [Sandbox](../../term_dictionary/term_sandbox.md) — process isolation/confinement; relevance: root cause is snap AppArmor confinement interfering with browser spawn; `--no-sandbox` is the fix flag.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the isolation runtime behind a sandbox; relevance: snap confinement is the offending sandbox backend; the fix swaps to an unsandboxed `.deb` Chrome.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional socket transport; relevance: CDP `ws://`/`wss://` endpoints carry the DevTools socket the config reference lists alongside `http`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: the product whose `openclaw.json` browser config + `openclaw browser start` commands this runbook edits.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class OpenClaw hosts; relevance: browser control is one of the agent capabilities this troubleshooting restores.

**Docs**
- [oc_tools_browser_login](oc_tools_browser_login.md) — manual login for the openclaw profile (planned, this series, note 2); relevance: same managed `openclaw` profile + host-browser theme; sibling runbook.
- [oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting](oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting.md) — split-host remote-CDP triage (planned, this series, note 3); relevance: the remote-CDP analog of this local-CDP startup failure; shares `cdpUrl`/`attachOnly`.
- [oc_tools_browser](../openclaw/oc_tools_browser.md) — the main browser tool reference (planned, to01); relevance: this page's `## Related` links back to the browser tool home.
- [cc_chrome_setup_and_troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — Claude Code Chrome setup + CDP troubleshooting; relevance: the closest cross-tool analog — same Chrome/CDP launch-failure class on a sibling agent.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Claude Code browser automation; relevance: documents the same headless-Chrome control surface the OpenClaw browser server exposes.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: sister-agent install/launch path for browser control, including executable-path resolution.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — managed vs attach backends; relevance: same managed-vs-attach-only distinction this page's Solution 2 uses.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — browser-process supervision/recovery; relevance: stale-Singleton-lock removal + relaunch retry mirrors the supervisor lifecycle.
- [cc_computer_use](../claude_code/cc_computer_use.md) — agent computer/browser control; relevance: the broader capability family the OpenClaw browser tool belongs to.
- [cc_sandbox_limitations_and_troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — sandbox constraints + failure triage; relevance: the root cause is snap AppArmor sandbox confinement blocking the Chrome spawn — same sandbox-confinement-breaks-a-subprocess failure class this page works around with `--no-sandbox`/unsandboxed `.deb`.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root; relevance: hosts the browser config schema this runbook edits.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugins/extensions home; relevance: the browser plugin lives in extensions.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway service; relevance: the gateway launches/monitors the browser-control server on the CDP port.

**Snippets** (`../../code_snippets/`)
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP connect/launch code; relevance: the implementation that connects to `--remote-debugging-port`.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session/profile lifecycle; relevance: managed `openclaw` profile + user-data-dir handling.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — launch/monitor supervisor; relevance: the spawn-and-monitor path that emits "Failed to start Chrome CDP".
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — stale-lock recovery + retry; relevance: removing `Singleton*` locks and retrying once, exactly this page's failure note.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — navigate/open-tab; relevance: backs `openclaw browser open` verification step.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: a post-launch action proving the browser works.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM snapshot/query; relevance: `snapshot`/tabs actions confirmed after a successful launch.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser plugin tool dispatch; relevance: how a browser tool call routes into the plugin that owns the CDP session.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway startup/auth; relevance: the gateway boot path that brings up the browser-control HTTP endpoint on `:18791`.

### oc_tools_browser_login (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: manual login establishes the authenticated session the browser-automation tool then drives.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer session credential; relevance: the page warns against giving the model credentials; sign-in mints the session token the `openclaw` profile reuses.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/sign-in; relevance: the page is about the human sign-in flow vs anti-bot defenses on automated logins.
- [Sandbox](../../term_dictionary/term_sandbox.md) — agent process isolation; relevance: "Sandboxing + host browser access" section — sandboxed sessions trigger more bot detection.
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: `profile="user"`/host-control is a CDP-vs-Chrome-MCP profile choice.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: documents `openclaw browser start/open --browser-profile` + `agents.defaults.sandbox.browser.allowHostControl` config.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class; relevance: the agent's `browser` tool calls target the host/sandbox browser.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — which surface/profile an action binds to; relevance: `allowHostControl` + `profile="user"` decide host-vs-sandbox browser binding.

**Docs**
- [oc_tools_browser_linux_troubleshooting](oc_tools_browser_linux_troubleshooting.md) — Linux CDP startup runbook (planned, this series, note 1); relevance: same managed `openclaw` profile; sibling browser page.
- [oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting](oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting.md) — split-host remote CDP (planned, this series, note 3); relevance: `existing-session`/`user` vs raw-CDP choice mirrors this page's profile selection.
- [oc_tools_browser](../openclaw/oc_tools_browser.md) — main browser tool (planned, to01); relevance: this page's "Back to the main browser docs" link.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Claude Code browser automation; relevance: same human-login-then-automate pattern for a dedicated browser profile.
- [cc_computer_use_safety](../claude_code/cc_computer_use_safety.md) — safety for agent browser/computer use; relevance: the "do not give the model your credentials" + anti-bot guidance is a safety analog.
- [hermes_browser_automation_setup](../hermes_agent/hermes_browser_automation_setup.md) — Hermes browser setup; relevance: sister-agent profile/login setup.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation under sandbox; relevance: host-browser-access-under-sandbox is a credential-isolation decision.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permission policy; relevance: `allowHostControl` is the sandbox-escape permission this page grants.
- [pi_security_model](../pi/pi_security_model.md) — Pi agent security model; relevance: cross-agent framing of sandboxed-vs-host capability grants.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — managed credential/session pools; relevance: the manual-sign-in session stored on the dedicated `openclaw` profile is exactly a managed credential the agent reuses without ever holding the raw secret.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root; relevance: `openclaw browser` CLI + browser-profile config.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin home; relevance: the browser tool the login feeds.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox/host-access policy; relevance: enforces `sandbox.browser.allowHostControl`.

**Snippets** (`../../code_snippets/`)
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — profile/session lifecycle; relevance: dedicated-profile selection + reuse this page configures.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — open/navigate; relevance: backs `openclaw browser open https://x.com`.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM read/search; relevance: read/search-threads flow on X/Twitter via the host browser.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser tool dispatch; relevance: routing a `browser` call to host vs sandbox.
- [snippet_hermes_agent_tools_browser_camofox](../../code_snippets/snippet_hermes_agent_tools_browser_camofox.md) — anti-detection browser backend; relevance: bot-detection avoidance this page warns about for strict sites.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential file handling; relevance: keeping the human's credentials out of the model/sandbox.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: host-vs-sandbox auth-mode resolution for the browser tool.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret/credential surfacing; relevance: how session credentials are (not) surfaced to the agent.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: precedence for where the browser session's auth comes from.

### oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: the page is raw remote CDP from WSL2 to a Windows Chrome `:9222` endpoint.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — agent browser control; relevance: the capability being made to cross the WSL2/Windows boundary.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: Option 2 is host-local Chrome MCP vs Option 1 raw remote CDP.
- [WebSocket](../../term_dictionary/term_websocket.md) — DevTools socket transport; relevance: `ws://`/`wss://` `cdpUrl` + the "CDP websocket not reachable" error class.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — port-forward/proxy layer; relevance: WSL2→Windows reachability often needs port forwarding/local proxying (Layer 2 fix).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: configures `browser.profiles.remote.cdpUrl` + Control UI at `:18789`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: the WSL2/Windows split is the host boundary browser transport must cross.
- [Authentication](../../term_dictionary/term_authentication.md) — token/pairing auth; relevance: `token_missing`/`pairing required`/`control-ui-insecure-auth` are Control-UI auth-layer failures the triage separates from CDP.

**Docs**
- [oc_tools_browser_linux_troubleshooting](oc_tools_browser_linux_troubleshooting.md) — local Linux CDP runbook (planned, this series, note 1); relevance: local-CDP sibling of this remote-CDP page.
- [oc_tools_browser_login](oc_tools_browser_login.md) — login/profile selection (planned, this series, note 2); relevance: `existing-session`/`user`-vs-remote profile choice overlaps.
- [oc_tools_browser_control](../openclaw/oc_tools_browser_control.md) — browser-control reference (planned, to01); relevance: the Control-UI rule + browser-profile config home.
- [cc_chrome_setup_and_troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — Chrome CDP setup/troubleshooting; relevance: the cross-tool remote-debugging-port setup analog.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — managed/attach/remote backends; relevance: `attachOnly: true` for an externally-managed remote browser.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — connect/recover supervision; relevance: "not reachable after start" reachability retries.
- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Claude Code browser control; relevance: same CDP-endpoint control surface across hosts.
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — gateway↔tool transport; relevance: gateway-side routing of the cross-host browser transport.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote-host agent control; relevance: cross-host control framing for the split WSL2/Windows setup.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote desktop/browser backend on another host; relevance: the directest sister-agent analog of attaching to an externally-managed browser across a host boundary (Windows Chrome `:9222` from WSL2), including reachability/forwarding.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway + Control UI; relevance: `gateway.controlUi.allowedOrigins`, bind, trusted-proxy behavior all live here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — browser plugin; relevance: the remote-CDP browser profile transport.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — root; relevance: `browser.profiles.*` config schema + `openclaw browser` CLI.

**Snippets** (`../../code_snippets/`)
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP connect; relevance: connecting to a `cdpUrl` HTTP/WS endpoint, the core of Layer 3/5.
- [snippet_hermes_agent_tools_browser_supervisor_recovery](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_recovery.md) — reachability retry/recovery; relevance: "Remote CDP not reachable" retry path.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — profile lifecycle; relevance: the `remote` profile with `attachOnly`.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control-UI auth ticketing; relevance: separates `token_missing`/insecure-auth from CDP transport (Layer 4).
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: origin/token/pairing checks the triage layer-isolates.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy-aware connect; relevance: WSL2→Windows proxying/port-forward reachability.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener bind; relevance: the gateway listening on `127.0.0.1:18789` for the Control UI.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser dispatch; relevance: routing a `browser` call to the `remote` CDP profile.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP/MCP; relevance: the host-local Chrome MCP (Option 2) loopback path vs raw remote CDP.
- [snippet_hermes_agent_cli_gateway_pid_discovery](../../code_snippets/snippet_hermes_agent_cli_gateway_pid_discovery.md) — gateway endpoint discovery; relevance: confirming the gateway/CDP endpoints during layered validation.

### oc_tools_btw (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [Subagent](../../term_dictionary/term_subagent.md) — isolated child agent run; relevance: `/btw` runs a separate ephemeral one-shot side query off the parent session.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — off-main side conversation; relevance: BTW is exactly a side-result not written to main transcript history.
- [Context Window](../../term_dictionary/term_context_window.md) — the model's active context; relevance: BTW snapshots current session context as background-only without polluting future context.
- [Compaction](../../term_dictionary/term_compaction.md) — context pruning/summarization; relevance: BTW's "no future context pollution" is the inverse goal of compaction — keep the side answer out of the budget.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — slash-command directive; relevance: `/btw` (alias `/side`) is a native slash command.
- [Agent Steering](../../term_dictionary/term_agent_steering.md) — injecting guidance into an active run; relevance: BTW is contrasted with `/steer`; explicitly tells the model NOT to steer the parent conversation.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: BTW emits `chat.side_result` at the Gateway protocol level across channels/TUI/Control UI.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class; relevance: BTW is modeled after Claude Code's `/btw` adapted to OpenClaw's multi-channel agent harness.

**Docs**
- [oc_tools_slash_commands](../openclaw/oc_tools_slash_commands.md) — native command catalog (planned, to07); relevance: this page's `## Related` Slash-commands card; `/btw` is one such directive.
- [oc_tools_steer](../openclaw/oc_tools_steer.md) — inject a steering message (planned, to06/to07); relevance: this page's Steer card; the contrast tool to BTW.
- [oc_tools_thinking](../openclaw/oc_tools_thinking.md) — reasoning-effort levels (planned, to07); relevance: this page's Thinking card — effort for the side-question model call.
- [cc_create_a_subagent](../claude_code/cc_create_a_subagent.md) — Claude Code subagent creation; relevance: BTW's "separate one-shot side query off the same context" is the subagent analog.
- [cc_forked_subagents](../claude_code/cc_forked_subagents.md) — forked subagents from current context; relevance: the Codex-harness path forks the active app-server thread as an ephemeral side thread.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — what occupies context; relevance: BTW supplies the in-flight prompt as background context only.
- [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — persistence across compaction/reload; relevance: BTW "does not survive a reload" — the opposite persistence contract.
- [cc_interactive_session_features](../claude_code/cc_interactive_session_features.md) — interactive session directives; relevance: ephemeral inline TUI side-answer behavior (dismissible, not replayed).
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — sister-agent side/delegate runs; relevance: cross-agent framing of an isolated side query that doesn't resume the parent task.
- [hermes_guide_delegation_patterns](../hermes_agent/hermes_guide_delegation_patterns.md) — when/how to spin off a delegated run; relevance: the decision pattern for offloading a one-shot side question to an ephemeral run instead of polluting the parent thread — exactly BTW's "ask on the side, don't steer" contract.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent harness; relevance: the harness that runs the BTW side query + transport selection.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session transcript persistence; relevance: BTW deliberately bypasses transcript history + `chat.history` here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway protocol; relevance: `chat` vs `chat.side_result` event separation lives at the gateway.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_btw_harness_transcript](../../code_snippets/snippet_openclaw_agents_btw_harness_transcript.md) — BTW transcript projection; relevance: the exact harness code that snapshots session context as background-only.
- [snippet_openclaw_agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — BTW context sanitize; relevance: seeding sanitized conversation context into the fresh one-shot side query.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event emission; relevance: `chat` vs `chat.side_result` event handling + `chat.history` exclusion.
- [snippet_openclaw_acp_spawn_thread_binding](../../code_snippets/snippet_openclaw_acp_spawn_thread_binding.md) — thread fork/binding; relevance: Codex-harness BTW forks the active app-server thread as an ephemeral side thread.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — ephemeral subagent spawn; relevance: the spawn path for an isolated one-shot side run.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime/harness selection; relevance: native-harness vs CLI-runtime-alias BTW transport branching.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool bundling/policy; relevance: BTW disables OpenClaw MCP tool bundling for the one-shot CLI invocation.
- [snippet_hermes_agent_core_conversation_loop_msg_prep](../../code_snippets/snippet_hermes_agent_core_conversation_loop_msg_prep.md) — message-state prep; relevance: snapshotting the current message state as side-query background.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session reset/no-persist hooks; relevance: leaving the main run alone + no transcript persistence after the side answer.

### oc_tools_code_execution (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — the agent code-run capability; relevance: this page IS the `code_execution` tool reference.
- [Code Interpreter](../../term_dictionary/term_code_interpreter.md) — sandboxed analysis-code runner; relevance: `code_execution` is xAI's remote code-interpreter (calc/tabulation/stats/chart analysis).
- [Python](../../term_dictionary/term_python.md) — the runtime language; relevance: `code_execution` runs sandboxed remote Python.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: it runs Python in xAI's remote sandbox, not local process execution.
- [xAI](../../term_dictionary/term_xai.md) — the Grok provider; relevance: registered by the bundled `xai` plugin, dispatched to `api.x.ai/v1/responses`.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — the Responses-API shape; relevance: dispatches to the xAI Responses API endpoint (`/v1/responses`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: `code_execution` is a function-callable tool taking a single `task` parameter.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider-supplied tool plugin; relevance: it's contributed by the `xai` provider plugin under the `tools` contract.

**Docs**
- [oc_tools_exec](../openclaw/oc_tools_exec.md) — local shell exec tool (planned, to03); relevance: the page explicitly contrasts remote `code_execution` vs local `exec`.
- [oc_tools_web](../openclaw/oc_tools_web.md) — web/x_search/web_fetch tools (planned, to08); relevance: pipe `x_search`/`web_search` results into `code_execution`.
- [oc_tools_exec_approvals](../openclaw/oc_tools_exec_approvals.md) — exec allow/deny policy (planned, to03); relevance: this page's Exec-approvals card.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — agent code-execution tool behavior; relevance: the closest cross-tool analog of a model-invoked code runner.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox FS/network isolation; relevance: "no local files / no workspace / remote-only" matches sandbox isolation guarantees.
- [cc_sandboxed_bash_tool_setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — sandboxed code-run setup; relevance: setup/enable/restart pattern for a sandboxed execution tool.
- [cc_sdk_python_tool_io_and_sandbox](../claude_code/cc_sdk_python_tool_io_and_sandbox.md) — Python tool I/O + sandbox; relevance: single-`task` Python invocation + sandboxed I/O model.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — local vs remote exec backends; relevance: remote-vs-local execution backend distinction.
- [pi_containerization](../pi/pi_containerization.md) — Pi sandboxed runtime; relevance: cross-agent framing of remote/contained code execution.
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — where agent code actually runs; relevance: enumerates the local-vs-remote/managed execution-environment choices that frame `code_execution` as xAI's *remote* sandbox (no local files/workspace) vs the local `exec` tool.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool catalog/dispatch; relevance: `code_execution` shows up in the agent tool list once the xAI plugin registers.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — provider plugins home; relevance: the bundled `xai` plugin that registers the tool lives in extensions.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec/dangerous-tool policy; relevance: deny/allow gating for code-execution-class tools.

**Snippets** (`../../code_snippets/`)
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed code-exec; relevance: the sandboxed remote-Python execution implementation.
- [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — exec result handling; relevance: structured JSON result / error surface like `missing_xai_api_key`.
- [snippet_hermes_agent_tools_code_exec_languages](../../code_snippets/snippet_hermes_agent_tools_code_exec_languages.md) — language selection; relevance: Python remote-analysis runtime.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool registration/catalog; relevance: tool appears in the catalog after `xai` re-registers with `enabled: true`.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool enable/policy; relevance: `codeExecution.enabled` gating.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/FS policy; relevance: the no-local-files constraint the page states.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny-list; relevance: code-execution-class deny gating.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: the bundled `xai` provider plugin registration path.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential resolution; relevance: xAI auth profile vs `XAI_API_KEY` vs plugin config precedence.
- [snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md) — request timeout/limits; relevance: 30s default timeout + `maxTurns` internal-limit handling.

### oc_tools_creating_skills (8t · 10s · 11d)

**Terms** (`../../term_dictionary/`)
- [Skills](../../term_dictionary/term_skills.md) — agent SKILL.md capability units; relevance: the page teaches authoring SKILL.md skills end to end.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — the SKILL.md frontmatter contract; relevance: the Required/Optional fields reference is the manifest spec.
- [Skills Hub](../../term_dictionary/term_skills_hub.md) — skill registry/marketplace; relevance: publishing to ClawHub (the skills hub) is the final section.
- [Atomic Skill](../../term_dictionary/term_atomic_skill.md) — one-purpose skill granularity; relevance: "be concise, instruct what to do" best-practice = atomic single-purpose skills.
- [Skill Curator](../../term_dictionary/term_skill_curator.md) — operator review/proposal flow; relevance: Skill Workshop propose→inspect→apply is the curation/review path.
- [Progressive Disclosure](../../term_dictionary/term_progressive_disclosure.md) — load skills only when relevant; relevance: conditional activation/gating (`requires.bins/env`, `disable-model-invocation`) gates when a skill loads.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin packaging metadata; relevance: plugins can ship skills; gating `metadata.openclaw` mirrors plugin manifest fields.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw skills list/workshop`, watcher, and loading precedence are OpenClaw mechanics.

**Docs**
- [oc_tools_skills](../openclaw/oc_tools_skills.md) — skills reference: loading order, gating (planned, to07); relevance: this page links to it for loading-order + gating details.
- [oc_tools_skill_workshop](../openclaw/oc_tools_skill_workshop.md) — proposal queue (planned, to06); relevance: this page's Skill Workshop propose-flow card.
- [oc_tools_skills_config](../openclaw/oc_tools_skills_config.md) — full `skills.*` schema (planned, to07); relevance: `skills.entries.*` apiKey/env wiring referenced here.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — Claude Code skill creation; relevance: the directest cross-tool authoring analog (directory + SKILL.md + frontmatter).
- [cc_skill_frontmatter_reference](../claude_code/cc_skill_frontmatter_reference.md) — skill frontmatter fields; relevance: maps to the Required/Optional SKILL.md field tables.
- [cc_skill_invocation_and_lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — skill load/invoke lifecycle; relevance: watcher reload, `/skill name`, model-vs-user invocation.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — skills concept overview; relevance: "skills teach the agent how/when to use tools" framing.
- [hermes_creating_skill_format](../hermes_agent/hermes_creating_skill_format.md) — sister-agent SKILL.md format; relevance: near-identical name/description/gating frontmatter spec.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — sister-agent skill publish; relevance: the publish-to-hub flow analog of ClawHub publishing.
- [pi_skills](../pi/pi_skills.md) — Pi agent skills; relevance: cross-agent skill-authoring model.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: SKILL.md loading, gating eval, watcher, and `openclaw skills` commands live here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugins that ship skills; relevance: "plugins can ship skills alongside tools".
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — root; relevance: workspace `skills/` roots + precedence order.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md manifest parse; relevance: the name/description/metadata frontmatter contract this page documents.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — gating evaluator; relevance: `requires.bins/anyBins/env/config`, `os`, `always` conditional activation.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill selection/planner; relevance: which skills get included in the system prompt vs `/skill`-only.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — command-dispatch tool descriptor; relevance: `command-dispatch: tool` + `command-tool`/`command-arg-mode` routing.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — submitted-skill security scan; relevance: safety validation before a skill/proposal goes live.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — frontmatter parsing; relevance: name/description/metadata extraction.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skill install CLI; relevance: `openclaw skills install clawhub-publish` install flow.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skill validation; relevance: naming rules + manifest validity checks.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — hub registry; relevance: ClawHub/skills-hub publish + browse.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin/skill load lifecycle; relevance: watcher reload + new-session refresh of the skill list.

### oc_tools_diffs_usage (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `diffs` is a function-callable tool with a typed input schema (before/after/patch/mode/...).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin packaging/config; relevance: `diffs` is an optional plugin; `plugins.entries.diffs.*` config + defaults.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin-contributed capability; relevance: the diffs plugin ships a tool + companion skill + prompt-injection hook.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin authoring surface; relevance: the diffs plugin uses the `before_prompt_build` hook + tool contract from the plugin SDK.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool schema/contract; relevance: the Tool input reference is the diffs tool descriptor (typed `ParamField`s + defaults).
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool registration; relevance: enabling the plugin registers `diffs` into the agent's tool set.
- [Skills](../../term_dictionary/term_skills.md) — companion-skill instructions; relevance: the plugin exposes a detailed companion skill for fuller agent instructions.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw plugins install diffs`, system-prompt guidance injection, and viewer-URL config are OpenClaw mechanics.

**Docs**
- [oc_tools_diffs_viewer_security](oc_tools_diffs_viewer_security.md) — viewer artifact + security model (planned, this series, note 8); relevance: the split sibling — output `details`/lifecycle/hardening this usage note hands off to.
- [oc_tools_plugin](../openclaw/oc_tools_plugin.md) — plugin tool overview (planned, to06); relevance: this page's `## Related` Plugins link; install/enable plugin lifecycle.
- [oc_tools_browser](../openclaw/oc_tools_browser.md) — browser tool (planned, to01); relevance: this page's Related Browser link; file mode needs a Chromium browser.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in agent tools; relevance: a function-callable tool with a typed input schema, cross-tool analog.
- [cc_sdk_custom_tool_definition](../claude_code/cc_sdk_custom_tool_definition.md) — defining a typed custom tool; relevance: the diffs tool-input schema is a typed tool definition.
- [cc_desktop_diff_review_and_pr](../claude_code/cc_desktop_diff_review_and_pr.md) — diff review UI; relevance: the directest functional analog — rendering before/after diffs for review.
- [cc_plugin_marketplace_walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — plugin install/enable; relevance: install-then-enable plugin flow analog.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — sister-agent built-in plugins; relevance: an optional bundled plugin tool with config defaults.
- [hermes_adding_built_in_tool](../hermes_agent/hermes_adding_built_in_tool.md) — adding a typed tool; relevance: typed tool-input + defaults authoring analog.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — what a plugin can ship (tools/skills/hooks); relevance: the `diffs` plugin ships exactly that bundle — a tool + companion skill + a `before_prompt_build` prompt-injection hook — so this maps the plugin-component model the usage note assembles.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin tool home; relevance: the `diffs` plugin + companion skill + language-pack live in extensions.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool catalog/dispatch; relevance: a `diffs` call routes through the agent tool dispatcher.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — root; relevance: `plugins.entries.diffs.*` config schema + syntax-highlighting language set.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor/contract; relevance: the typed-input descriptor pattern the diffs Tool input reference follows.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool registration; relevance: enabling the plugin registers `diffs` into the catalog.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool enable/policy; relevance: `plugins.entries.diffs.enabled` + per-call vs default precedence.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/enable lifecycle; relevance: `openclaw plugins install diffs` + enable + companion-skill exposure.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: how an optional plugin tool registers with input validation.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — plugin tool dispatch; relevance: routing a plugin-tool call (the dispatch path a `diffs` call uses).
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — plugin hook handler; relevance: the `before_prompt_build` system-guidance injection hook (`allowPromptInjection`).
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hooks; relevance: prompt-injection-into-system-prompt hook analog.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — plugin registry; relevance: optional-plugin registration + defaults.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP route registration; relevance: the plugin's `/plugins/diffs/*` viewer/asset routes (also feeds note 8).

### oc_tools_diffs_viewer_security (8t · 10s · 10d)

**Terms** (`../../term_dictionary/`)
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — outbound-request denial; relevance: file-render is deny-by-default; only local viewer assets allowed, external network blocked.
- [Throttling](../../term_dictionary/term_throttling.md) — request rate limiting; relevance: remote-miss throttling (40 failures/60s, 60s lockout, `429`).
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-frequency caps; relevance: the `429 Too Many Requests` lockout on viewer-route remote misses.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: `gateway.trustedProxies` / Tailscale Serve loopback proxy interaction + forwarded-client-IP fail-closed behavior.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: artifacts stored in a temp subfolder; file-render runs in a constrained browser request scope.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — headless browser rendering; relevance: file mode (`png`/`pdf`) needs a Chromium-compatible browser via Playwright.
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: the Chromium/Playwright render path that produces the file artifact.
- [Function Calling](../../term_dictionary/term_function_calling.md) — typed tool output; relevance: the `details` output contract (viewer/file/compat fields, mode behavior) is the tool's structured return.

**Docs**
- [oc_tools_diffs_usage](oc_tools_diffs_usage.md) — diffs usage/config (planned, this series, note 7); relevance: the split sibling — install/enable/modes/input feeding this output+security note.
- [oc_tools_plugin](../openclaw/oc_tools_plugin.md) — plugin overview (planned, to06); relevance: this page's Related Plugins link; the plugin owning the viewer routes.
- [oc_web_control_ui](../openclaw/oc_web_control_ui.md) — Control UI / canvas (planned, wb01); relevance: `mode: "view"` opens `viewerUrl` with `canvas present`.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — FS/network isolation; relevance: loopback-only + outbound `connect-src 'none'` + external-network-blocked mirrors isolation defaults.
- [cc_desktop_diff_review_and_pr](../claude_code/cc_desktop_diff_review_and_pr.md) — diff review/render; relevance: the diff-render-and-present functional analog.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web-surface security limits; relevance: CSP, loopback binding, and throttling are the same hardening class.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation/credential hardening; relevance: deny-by-default network + don't-send-secrets operational guidance.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool outputs; relevance: structured `details` output contract analog.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote access controls; relevance: `allowRemoteViewer` + `viewerBaseUrl`/`baseUrl`/custom-bind remote-access decision.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — HTTP route hardening (auth, bind, proxy trust, rate limits); relevance: the directest analog for the `/plugins/diffs/view/{artifactId}/{token}` viewer-route security — tokenized routes, loopback bind, `trustedProxies` fail-closed, and the 429 remote-miss throttle.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — viewer/network hardening; relevance: loopback-only, CSP, deny-by-default network, throttling all enforced here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — viewer route + bind/proxy; relevance: `/plugins/diffs/view/...` route, bind mode/`customBindHost`, `trustedProxies` fail-closed.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — diffs plugin home; relevance: the plugin that creates/cleans the viewer artifacts + assets.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP route; relevance: the `/plugins/diffs/view/{artifactId}/{token}` + assets routes.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP binding; relevance: viewer defaults to loopback `127.0.0.1` unless overridden.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — trusted-proxy handling; relevance: `trustedProxies` loopback + forwarded-IP fail-closed for same-host proxies.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit/lockout policy; relevance: 40-misses/60s throttle + 60s `429` lockout.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — tokenized route authorization; relevance: strict artifact-ID + token validation on viewer paths.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime security audit; relevance: deny-by-default + hardening posture for rendered artifacts.
- [snippet_hermes_agent_core_file_safety](../../code_snippets/snippet_hermes_agent_core_file_safety.md) — file artifact safety; relevance: TTL/temp-folder lifecycle + size/page caps on rendered files.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — headless render/screenshot; relevance: the Chromium render path producing png/pdf with safety MP caps.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — constrained render environment; relevance: screenshot-browser request routing deny-by-default + local-assets-only.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — request handler/CSP; relevance: the viewer-response CSP (`default-src 'none'`, self-only scripts, no `connect-src`).

## Undigested Terms Plan

Per master: OpenClaw vocabulary that is the subject of a doc page is digested as the `oc_*` doc note itself, NOT a new `term_dictionary` entry; the only term_dictionary interaction is **linking existing** terms. Expected **0 new `term_dictionary` captures**. Augment re-runs the Step 2d new-term scan.

| Term (from these pages) | Disposition |
|---|---|
| browser control / CDP / remote CDP | Link existing `term_browser_automation` + `term_cdp`; concept documented in notes 1/2/3 — no new term. |
| Control UI / browser profile / attach-only mode | Documented in-note (notes 1/3) as operational config; not promoted (too specific/operational). |
| `/btw` (by-the-way ephemeral side question) | Digested AS the doc note `oc_tools_btw` (note 4); link `term_subagent`/`term_context_window`/`term_command_pattern`. No new term. |
| `code_execution` tool / sandboxed remote Python / xAI | Digested AS `oc_tools_code_execution` (note 5); link existing `term_code_execution_tool` + `term_python` + `term_sandbox` + `term_xai`. No new term. |
| skill / SKILL.md / `{baseDir}` / conditional activation / Skill Workshop | Digested AS `oc_tools_creating_skills` (note 6); link existing `term_skills` + `term_skill_manifest` + `term_skills_hub`. No new term. |
| ClawHub (publishing target) | Link-out to cw01/cw02 (planned ClawHub sub-plans) + `term_skills_hub`; not promoted here. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term with no existing note and no doc-page home appears. (Decision deferred to augment Step 2d re-scan; if a reviewer judges `diffs`/`diff viewer` reusable enough, the best-fit glossary would be `acronym_glossary_agentic_dev.md`, but the master precedent is to digest tool vocabulary as doc notes, not term notes.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean (YAML field order, tags begin resource/documentation/openclaw, `## Overview` + `## Related Notes` present, bold footer). |
| G2 | Grounding | Each note's claims diff-verified against `inbox/openclaw_docs/tools/<page>.md`; config/command snippets verbatim; no invented fields. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code fences; one building_block; every source H2/H3 mapped (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected term notes + relevant `repo_openclaw*` + sibling `oc_*` + other vault notes, each an indexed `[text](path.md)` link with a relevance statement. |
| G5 | Ghost-reference | Every cited EXISTING target resolves in DB; ghosts detected → redirected/dropped (the `term_diff_different_item` mismatch is pre-flagged for removal). |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after reindex (relative paths from `resources/documentation/openclaw/`). |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` rows + `repo_openclaw*`/`term_*` inlinks (see Inlinks section). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_browser_linux_troubleshooting oc_tools_browser_login oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting oc_tools_btw oc_tools_code_execution oc_tools_creating_skills oc_tools_diffs_usage oc_tools_diffs_viewer_security"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # sibling-prefix link present (G4/G7 sanity)
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n NO SIBLING $SIBLING_PREFIX LINK"
  # density caps (body words excl. frontmatter; code fences)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w, ${cb} code)"
done

# YAML frontmatter validation across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_browser_linux_troubleshooting | procedure | 500 | ≤6 (of 9 src) | ✅ |
| 2 | oc_tools_browser_login | procedure | 350 | ≤3 | ✅ |
| 3 | oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting | procedure | 700 | ≤5 | ✅ |
| 4 | oc_tools_btw | concept | 550 | ≤2 | ✅ |
| 5 | oc_tools_code_execution | procedure | 500 | ≤4 | ✅ |
| 6 | oc_tools_creating_skills | procedure | 650 | ≤5 | ✅ |
| 7 | oc_tools_diffs_usage | procedure | 650 | ≤4 | ✅ |
| 8 | oc_tools_diffs_viewer_security | model | 600 | ≤2 | ✅ |

No note approaches the 2,500w / 400-line / 6-fence caps. The 2,129w diffs.md splits (notes 7+8) so each half stays ~650/600w with ≤4 fences. browser-linux-troubleshooting (9 source fences) → note 1 keeps only the load-bearing install/`systemd` unit/config snippets (≤6).

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `0_entry_points/entry_openclaw_docs.md` (created as master pre-step W1, >30-note series ⇒ required) under the **Tools → to02** cluster (one row per note: filename · BB · 1-line description). Each note receives its entry-point back-link at finalization (satisfies G7/G8). No standalone entry point created by this sub-plan; W2–W5 hub/code-cross-link/glossary steps are master-owned.

## Inlinks (existing notes → new notes)

- `entry_openclaw_docs.md` (planned, master W1) → **all 8 notes** (primary anti-island guarantee).
- `repo_openclaw_extensions.md` → notes 1, 2, 6, 7, 8 (browser/diffs plugins + skills live in extensions).
- `repo_openclaw_gateway.md` → notes 1, 3, 8 (gateway-launched browser service + viewer route).
- `repo_openclaw_security.md` → notes 2, 5, 8 (sandbox/host-access + exec policy + viewer hardening).
- `repo_openclaw_agents.md` → notes 4, 5, 7 (tool catalog/dispatch + `/btw` harness).
- `repo_openclaw_skills.md` → note 6 (skills subsystem).
- `term_browser_automation.md` / `term_cdp.md` → notes 1, 2, 3, 8.
- `term_code_execution_tool.md` / `term_xai.md` → note 5.
- `term_skills.md` / `term_skill_manifest.md` → note 6.
- `term_subagent.md` → note 4.
- Snippet back-links (reciprocal): `snippet_openclaw_agents_btw_harness_transcript` / `snippet_openclaw_agents_btw_streamSimple_sanitize` → note 4; `snippet_openclaw_skills_manifest_format` → note 6; `snippet_openclaw_security_exec_filesystem_policy` → note 5.

## Pacing Rules (inherited from master)

One execution phase, 8 notes — within the ~30-agent fan-out cap. Re-read each source page before authoring; reproduce config/command snippets verbatim; one BB per note. `git pull --rebase --autostash origin main` before commit; commit + push per wave; no Claude co-author trailer. Reindex incrementally; verify `note_links` populated + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Source re-read (CP7 measured, body words excl. frontmatter):** browser-linux-troubleshooting 758w (plan 785), browser-login 306w (339), browser-wsl2-windows-remote-cdp-troubleshooting 1,017w (1,073), btw 794w (830), code-execution 654w (698), creating-skills 1,023w (1,099), diffs 2,076w (2,129). All within ±10% of plan estimates — no density under-estimation; no re-splits needed. The diffs.md split (notes 7+8) keeps each half ≤650/600w.

**What was LOCKED (replaced `## Candidate Cross-References` → `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_tools_browser_linux_troubleshooting | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_browser_login | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_browser_wsl2_windows_remote_cdp_troubleshooting | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_btw | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_code_execution | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_creating_skills | 8 | 10 | 11 (7/4) | 3 | ✅ |
| oc_tools_diffs_usage | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_tools_diffs_viewer_security | 8 | 10 | 10 (6/4) | 3 | ✅ |


**Ghost / false-positive resolution:**

**New-term candidates: NONE.** The Step 2d re-scan over all 7 re-read pages surfaced no genuinely cross-cutting, vault-reusable term lacking both an existing note and a doc-page home. Every page-subject term is digested AS its `oc_*` doc note; existing terms are LINKED. (If a future reviewer judged `diffs`/`diff viewer` reusable, best-fit glossary = `acronym_glossary_agentic_dev.md` — but master precedent overrides.) Undigested Terms Plan unchanged: 0 new `term_dictionary` captures.

**Minor coverage note (non-blocking):** diffs.md also has a short `## Security config` H2 (`security.allowRemoteViewer` toggle) sitting between Plugin defaults and Artifact lifecycle. It falls cleanly under note 8's "Security model / viewer-file hardening" scope (the `allowRemoteViewer` flag is the remote-access toggle the Security model + Operational guidance + Troubleshooting all reference). Section Coverage Map line for note 8 ("Security model (viewer/file hardening)") covers it; flagged here so the executor maps it explicitly during G2 grounding.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + ≥10 snippets + ≥10 docs floors, per-link relevance) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 8 notes meet 8t/10s/10d (deterministic per-note count); every link carries `— <what> ; relevance: <why THIS note>`. |
| CP2 | 9-GATE per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link, G7/G8 discoverability. G5 references `/tessellum-fix-ghost-references`-class detection; ghost script in `## Validation Scripts`. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` contributes 8 rows to `0_entry_points/entry_openclaw_docs.md` (master W1, >30-note series ⇒ required); each note gets its entry-point back-link at finalization. |
| CP4 | Plan size manageable | **PASS** | 8 notes (≤30); single execution phase, within ~30-agent fan-out cap. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` + source-mirrored body + `## Related Notes` + `## References` + bold footer; YAML field order verified against target-dir precedent). |
| CP6 | Borderline density → split promoted | **PASS** | Only diffs.md (2,076w, mixed BB) borderline → already SPLIT into notes 7 (procedure) + 8 (model); all other pages <1,100w single-BB. No further splits. |
| CP7 | Source word counts measured (not guessed) | **PASS** | 7/7 pages re-measured this pass; all within ±10% of plan estimates (max delta diffs.md −2.5%). No >1.5× under-estimate. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` (7 rows, all dispositioned to link-existing / digest-as-doc-note, 0 new captures) + `## Term-Note Authoring Requirements` (N/A, 0 new terms, mandate inherited from master). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to specificity-audit. Collision audit run for all 8 planned doc notes against term_dictionary AND documentation/: no `oc_tools_*` slug duplicates an existing term/doc note. `term_diff_different_item` false-positive collision caught and dropped; no `term_diff`/`term_diff_viewer` exists. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` table maps every new note to ≥1 outside-folder inbound source (entry_openclaw_docs → all 8; `repo_openclaw*` + `term_*` + reciprocal snippet back-links per note); G7/G8 in the gate table; inlinks specified as an executed phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
