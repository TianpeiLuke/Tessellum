---
title: Sub-Plan B12A — Claude Code Docs: IDE & Desktop Surfaces
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["vs-code", "jetbrains", "desktop", "desktop-quickstart"]
---

# Sub-Plan B12A: IDE & Desktop Surfaces

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Authored from a fresh re-read of its 4 source pages, then run through `/tessellum-augment-digestion-plan`
> → `/tessellum-review-digestion-plan`. Structure mirrors the accepted exemplar
> [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring are inherited from
> the master; this file extends, never overrides.

## Scope

The 4 graphical-surface pages that document how to run Claude Code inside the two desktop IDEs (VS Code
and JetBrains) and the standalone Claude Desktop app (the Code tab). P2 (Phase B) — built on the Phase A
cores (permissions, MCP, skills, subagents, sessions, context window) which these surfaces all reuse with
graphical front-ends. `desktop.md` is the largest page in the corpus (8,626 words) and forces the heaviest
splitting of any sub-plan in this batch.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 16,531 measured words. **Planned: 11 notes.**

## Content Strategy

- **Prioritize**: the surface-specific operating model of each GUI — how install/launch differs, the
  graphical permission-mode selector, diff/PR review, pane layout, parallel-session-via-worktree isolation,
  computer use, and the desktop ↔ CLI shared-configuration contract. These are the facts a reader picks a
  surface by.
- **Group**: `desktop.md` (8.6Kw, ~14 H2) splits by operating concern (getting-started+sessions / permission
  modes / diff+review+PR / workspace panes / computer use / parallel+dispatch+remote / extend / environment /
  enterprise / CLI-comparison). `vs-code.md` (5.3Kw) splits into setup+prompt-box vs config+CLI-relationship.
  `jetbrains.md` and `desktop-quickstart.md` are each one note.
- **Skip / link-out (own other sub-plans)**: permission *concepts* → B05A (`permissions.md`/`permission-modes.md`);
  sandboxing → B05B; MCP internals → B08A; skills/commands/plugins concepts → B06/B09A; sessions/checkpointing/
  worktree concepts → B02B/B10B; computer-use depth → B13A (`computer-use.md`); Chrome → B13A; scheduled tasks →
  B11 (`desktop-scheduled-tasks.md`); Remote Control / Dispatch surface comparison → B12B; cloud sessions /
  web → B12B (`claude-code-on-the-web.md`); third-party providers → B14A; auth/SSO/network/managed-settings
  depth → B14B; data handling → B16; errors → B17. These are referenced via links, never duplicated.
- **Undigested terms**: per Pattern B, no new `cc_` glossary notes and no new `term_dictionary` captures —
  vocabulary routes to existing term notes / home sub-plans (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| vs-code | /vs-code | 5,344 | 9 | 12 | 13 | procedure |
| jetbrains | /jetbrains | 1,185 | 5 | 7 | 6 | procedure |
| desktop | /desktop | 8,626 | 7 | 11 | 26 | procedure |
| desktop-quickstart | /desktop-quickstart | 1,376 | 0 | 4 | 0 | procedure |

> **H2 lists (document order):**
> - **vs-code**: Prerequisites · Install the extension · Get started (H3 4 Steps) · Use the prompt box (H3 Reference files and folders, Resume past conversations, Resume cloud sessions from Claude.ai, Check account and usage) · Customize your workflow (H3 Choose where Claude lives, Run multiple conversations, Switch to terminal mode) · Manage plugins (H3 Install plugins, Manage marketplaces) · Automate browser tasks with Chrome · VS Code commands and shortcuts (H3 Launch a VS Code tab from other tools) · Configure settings (H3 Extension settings) · VS Code extension vs. Claude Code CLI (H3 Rewind with checkpoints, Run CLI in VS Code, Switch between extension and CLI, Include terminal output in prompts, Monitor background processes, Connect to external tools with MCP) · Work with git (H3 Create commits and pull requests, Use git worktrees for parallel tasks) · Use third-party providers · Security and privacy (H3 The built-in IDE MCP server) · Fix common issues (H3 Extension won't install, Spark icon not visible, Cmd+Esc, Claude Code never responds) · Uninstall the extension · Next steps
> - **jetbrains**: Supported IDEs · Features · Installation · Usage (H3 From your IDE, From external terminals) · Configuration (H3 Claude Code settings, Plugin settings) · Special configurations (H3 Remote development, WSL configuration) · Troubleshooting (H3 Plugin not working, IDE not detected, Command not found) · Security considerations
> - **desktop**: Start a session · Work with code (H3 Use the prompt box, Add files and context, Choose a permission mode, Preview your app, Review changes with diff view, Review your code, Monitor pull request status) · Arrange your workspace (H3 Run commands in the terminal, Open and edit files, Open files in other apps, Switch view modes, Keyboard shortcuts, Check usage) · Let Claude use your computer (H3 When computer use applies, Enable computer use, App permissions) · Manage sessions (H3 Work in parallel with sessions, Ask a side question, Watch background tasks, Run long-running tasks remotely, Continue in another surface, Sessions from Dispatch) · Extend Claude Code (H3 Connect external tools, Use skills, Install plugins, Configure preview servers) · Environment configuration (H3 Local sessions, Cloud sessions, SSH sessions) · Enterprise configuration (H3 Admin console controls, Managed settings, Device management policies, Authentication and SSO, Data handling, Deployment) · Coming from the CLI? (H3 CLI flag equivalents, Shared configuration, Feature comparison, What's not available) · Troubleshooting (H3 9 issue sub-sections)
> - **desktop-quickstart**: (intro: three tabs Chat/Cowork/Code) · Install (H3 2 Steps) · Start your first session (H3 4 Steps) · Now what? · Coming from the CLI? · What's next

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **11 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_vs_code_extension.md` | procedure | vs-code: Prerequisites, Install, Get started (4 Steps), Uninstall, Fix common issues | 700 | Install the VS Code extension (Cursor / VSCode forks / Open VSX); the 4-step getting-started (open the Spark icon panel, sign in, prompt, review diffs); uninstall + the 4 common-issue fixes. Links permission modes → B05A. |
| 2 | `cc_vs_code_prompt_box_and_sessions.md` | procedure | vs-code: Use the prompt box (+H3s), Customize your workflow, Manage plugins, Automate browser tasks with Chrome | 650 | Prompt-box features (modes, command menu, context indicator, extended thinking, multi-line); @-mention files/folders; resume local + cloud (claude.ai) sessions; usage dialog; panel placement / multiple conversations / terminal mode; `/plugins` UI; `@browser`. |
| 3 | `cc_vs_code_settings_and_cli_relationship.md` | procedure | vs-code: Configure settings (+Extension settings table), VS Code commands and shortcuts (+Launch tab), VS Code extension vs. Claude Code CLI (+H3s), Work with git, Use third-party providers | 750 | Extension settings vs shared `~/.claude/settings.json`; the commands/shortcuts table + `vscode://` URI handler; CLI-vs-extension feature matrix, checkpoints/rewind, running the CLI in the integrated terminal, sharing history, `@terminal`, MCP via CLI; git commits/PRs + `--worktree`; third-party-provider setup (→ B14A). |
| 4 | `cc_vs_code_ide_mcp_server.md` | concept | vs-code: Security and privacy → The built-in IDE MCP server | 450 | The hidden `ide` MCP server the CLI auto-connects to: 127.0.0.1 random-port + per-activation auth token in `~/.claude/ide/`; the two model-visible tools (`mcp__ide__getDiagnostics`, `mcp__ide__executeCode`); Jupyter execute-always-asks Quick Pick; selection/open-file context + `Read` deny rules. |
| 5 | `cc_jetbrains_plugin.md` | procedure | jetbrains: (whole page) Supported IDEs, Features, Installation, Usage, Configuration, Special configurations, Troubleshooting, Security | 600 | The JetBrains plugin (IntelliJ/PyCharm/WebStorm/…): install CLI + plugin (no bundled CLI); `/ide` connect; diff/selection/diagnostic sharing; `/config` diff tool + plugin settings; remote-development + WSL2 firewall/mirrored-networking fixes; troubleshooting; auto-edit security note. |
| 6 | `cc_desktop_quickstart.md` | procedure | desktop-quickstart: (whole page) intro tabs, Install (2 Steps), Start your first session (4 Steps), Now what?, Coming from the CLI? | 650 | Get started with the Desktop app: download (macOS/Windows; not Linux), Chat/Cowork/Code tabs, install + open Code tab, the 4-step first session (Local/Remote/SSH env + folder, pick model, prompt, review/accept), then a "try next" tour pointing to the desktop reference sections. |
| 7 | `cc_desktop_overview_and_sessions.md` | procedure | desktop: intro, Start a session, Work with code → Use the prompt box + Add files and context; Manage sessions → Work in parallel, Ask a side question, Watch background tasks | 700 | The Code tab model: a session = own chat/folder/changes; start a session (Environment/Project/Model/Permission); prompt box + interrupt/steer; @mention + attachments; parallel sessions via per-session Git worktrees (storage/branch-prefix/auto-archive); side chats (`/btw`); the tasks pane (subagents / background commands / dynamic workflows). |
| 8 | `cc_desktop_permission_modes.md` | concept | desktop: Work with code → Choose a permission mode (incl. auto-mode availability + cloud-session note) | 450 | The 5 graphical permission modes (Ask permissions/Auto accept edits/Plan/Auto/Bypass) with settings keys and behavior; auto-mode availability (research preview, model requirements, Vertex AI gating); cloud-session mode mapping; `dontAsk` is CLI-only. Concept owner → B05A `permission-modes.md`. |
| 9 | `cc_desktop_diff_review_and_pr.md` | procedure | desktop: Work with code → Preview your app, Review changes with diff view, Review your code, Monitor pull request status; Extend → Configure preview servers (+Auto-verify, fields, port conflicts, examples) | 750 | Verify-and-review loop: app preview / auto-verify, diff view + inline line comments, `Review code` self-review (high-signal only), PR monitoring with auto-fix/auto-merge (needs `gh`); `.claude/launch.json` preview-server config (fields, `program` vs `runtimeExecutable`, `autoPort`, examples). |
| 10 | `cc_desktop_workspace_panes.md` | procedure | desktop: Arrange your workspace → Run commands in the terminal, Open and edit files, Open files in other apps, Switch view modes, Keyboard shortcuts, Check usage; Let Claude use your computer (+H3s) | 700 | Drag/resize pane layout (chat/diff/preview/terminal/file/plan/tasks/subagent); integrated terminal; file pane edit + open-in-other-apps; Normal/Verbose/Summary view modes; the Code-tab keyboard-shortcut table; usage ring; computer use (when it applies, enable on macOS/Windows, per-app access tiers, denied apps). Computer-use depth → B13A. |
| 11 | `cc_desktop_environments_extend_and_enterprise.md` | procedure | desktop: Manage sessions → Run long-running tasks remotely, Continue in another surface, Sessions from Dispatch; Extend Claude Code → Connect external tools, Use skills, Install plugins; Environment configuration (Local/Cloud/SSH); Enterprise configuration; Coming from the CLI? (Shared config, flag equivalents, feature comparison, what's not available) | 800 | Cloud/remote + continue-in-surface + Dispatch sessions (→ B12B/B11); connectors (MCP-with-GUI) / skills / plugins UI; Local/Cloud/SSH environment config incl. `sshConfigs`/`sshHostAllowlist` managed keys; enterprise admin-console + managed-settings + MDM; the desktop ↔ CLI shared-config contract, flag-equivalent + feature-comparison tables, what's-not-available list. |

**Estimate: 11 notes** — procedure ×9 (notes 1,2,3,5,6,7,9,10,11), concept ×2 (notes 4, 8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (16,531 words). New `cc_` notes: 11. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~7,000 (avg ~640/note). Code blocks: bounded ≤6/note (note 9 preview-server JSON examples are the densest; capped at 6 by trimming to 3 representative configs — see Density Re-Assessment).
- **Building Block Distribution**: procedure ×9 (notes 1,2,3,5,6,7,9,10,11) · concept ×2 (notes 4,8). No model/argument/empirical_observation — these pages are install/operate procedures plus two architecture/decision concepts (IDE MCP server, permission modes).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_vs_code_extension` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents how to install and launch Claude Code's own VS Code surface, so the product term is the definitional anchor for the extension being installed.
- [VS Code](../../term_dictionary/term_vscode.md) — The note is entirely about the VS Code (and forks) editor that hosts the extension — install path, Spark icon, Editor Toolbar, Restricted Mode — so the editor term grounds the host environment.
- [Cursor](../../term_dictionary/term_cursor.md) — The note's install section gives a dedicated `cursor:extension/...` link and lists Cursor among the VS Code forks the extension installs into, making Cursor a first-class supported host the note documents.
- [Cline](../../term_dictionary/term_cline.md) — The note's "Spark icon not visible" fix tells users to disable conflicting AI extensions like Cline; Cline is the comparable VS-Code-extension coding agent contextualizing the surface category.
- [AI-Assisted Development](../../term_dictionary/term_ai_assisted_development.md) — The note frames the extension as a native AI coding-assistance panel (inline diffs, plan review, @-mentions) inside the editor, the canonical AI-assisted-development integration this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The getting-started flow introduces the permission prompt on each edit (accept/reject/modify) and the diff-before-apply gate — the graduated-trust review model the term defines, here in graphical form.

### 2. `cc_vs_code_prompt_box_and_sessions` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the day-to-day prompt-box and session features of the Claude Code VS Code extension, so the product term anchors the surface whose UI is described.
- [VS Code](../../term_dictionary/term_vscode.md) — Every feature here (command menu, panel placement, multiple tabs, terminal mode, `/plugins` UI) is a VS-Code-specific presentation, so the editor term grounds the host.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's context-indicator feature shows how much of Claude's context window a prompt uses and offers `/compact`, directly surfacing the context-window concept this term defines.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — The note's extended-thinking toggle lets Claude spend more time reasoning and renders its reasoning as collapsible blocks — the chain-of-thought reasoning behavior the term covers (master maps "extended thinking" → this term).
- [Skills](../../term_dictionary/term_skills.md) — The command menu and `/plugins` interface let the user invoke skills and manage skill-bearing plugins from the prompt box, so the skills term grounds that capability.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The command menu's Customize section exposes MCP servers, and `@browser` connects the Chrome MCP integration — MCP underlies the external-tool features the note lists.

### 3. `cc_vs_code_settings_and_cli_relationship` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note maps the relationship between the Claude Code VS Code extension and the Claude Code CLI (shared settings, history, feature matrix), so the product term anchors both surfaces being compared.
- [VS Code](../../term_dictionary/term_vscode.md) — The extension-settings table, `vscode://` URI handler, and command list are VS-Code-specific, so the editor term grounds the host environment the note configures.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note's "Connect to external tools with MCP" section shows `claude mcp add` from the integrated terminal and `/mcp` management, making MCP a core part of the CLI-vs-extension capability boundary it documents.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The note covers checkpoints/rewind (fork conversation, rewind code) and shared conversation history across extension and CLI — the persisted session state and memory mechanism this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The CLI-vs-extension feature matrix is organized around which tools/commands each surface exposes, and `@terminal` feeds tool output back into prompts — the tool-use loop this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The shared `~/.claude/settings.json` the note configures holds allowed commands and permission rules that both surfaces honor — the settings-scoped graduated-trust controls this term covers.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — The note's "Work with git" section has Claude stage changes, write commit messages, and create pull requests, and the `--worktree` flag isolates parallel branches — the version-control-and-pipeline workflow this term defines.

### 4. `cc_vs_code_ide_mcp_server` (7 term notes)
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — This note documents a concrete local MCP server (named `ide`) that the CLI auto-connects to, including its transport, auth, and exposed tools — a direct instantiation of the MCP concept this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `ide` server is how the Claude Code CLI opens diffs in VS Code, reads selections for @-mentions, and runs Jupyter cells, so the product term anchors the surface integration described.
- [VS Code](../../term_dictionary/term_vscode.md) — The server runs inside the VS Code extension and exposes VS-Code-native capabilities (diagnostics from the Problems panel, the Jupyter kernel), so the editor term grounds the host.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note enumerates the two model-visible tools (`getDiagnostics`, `executeCode`) the CLI presents to Claude as callable tools — the function-calling/tool-use mechanism this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note's Jupyter "always asks first" Quick Pick and the `PreToolUse` allowlist interaction are graphical graduated-trust gates layered on top of permission rules, the trust-escalation model this term covers.
- [Deny-First](../../term_dictionary/term_deny_first.md) — The note instructs adding a `Read` deny rule for sensitive files (e.g. `.env`) so neither selected text nor open-file notice reaches Claude — the deny-rule-takes-precedence pattern this term defines.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The server binds to `127.0.0.1` on a random high port with a 0600 lock file in a 0700 directory, an isolation/least-exposure design analogous to the sandbox isolation boundary this term defines.

### 5. `cc_jetbrains_plugin` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the JetBrains-IDE surface of Claude Code (install, `/ide` connect, diff/selection sharing), so the product term anchors the integration being configured.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The JetBrains plugin connects to the running `claude` process the same way the VS Code IDE MCP server does (diff viewing, selection/diagnostic sharing over the IDE integration), so MCP grounds the integration mechanism.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Diagnostic sharing feeds the IDE's lint/syntax errors to Claude and diff viewing surfaces tool actions in the IDE — the tool-result feedback this term defines, here through the JetBrains integration.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note's security section warns that auto-edit mode in a JetBrains IDE can modify auto-executed config files and recommends manual approval mode — the graduated-trust escalation choice this term covers.
- [Deny-First](../../term_dictionary/term_deny_first.md) — The note states `Read` deny rules block selection/tab sharing for matching files, the deny-rule-wins precedence this term defines.
- [SSH](../../term_dictionary/term_ssh.md) — The Remote Development section requires installing the plugin on the remote host and the WSL2 fixes address host↔IDE connectivity — remote-host development scenarios the SSH term grounds.

### 6. `cc_desktop_quickstart` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the getting-started walkthrough for the Claude Desktop app's Code tab — Claude Code with a GUI — so the product term anchors the app being installed.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note describes the Cowork tab as an autonomous background agent working in a cloud VM and the Code tab's review-each-change flow — the autonomous-coding-agent operating modes this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The "review and accept changes" step and the Ask permissions / Auto accept / Plan mode tour are the graduated-trust escalation ladder this term defines, shown in the desktop GUI.
- [Skills](../../term_dictionary/term_skills.md) — The "use skills for repeatable tasks" tip (`/` or + → Slash commands for built-in/custom/plugin skills) introduces skills as the desktop's reusable-prompt mechanism this term defines.
- [SSH](../../term_dictionary/term_ssh.md) — The first-session environment choice offers Local/Remote/SSH, where SSH connects to a remote machine (servers, cloud VMs, dev containers) — the SSH remote-execution mode this term grounds.
- [Context Window](../../term_dictionary/term_context_window.md) — The note explains a session tracks its own context and changes, the per-session context window this term defines that keeps parallel tasks from interfering.

### 7. `cc_desktop_overview_and_sessions` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the core operating reference for the Claude Desktop Code tab, so the product term anchors the surface whose session model it documents.
- [Context Window](../../term_dictionary/term_context_window.md) — The note states each session tracks its own context independently and that Claude auto-summarizes when context fills (with `/compact`) — the per-session context window this term defines.
- [Compaction](../../term_dictionary/term_compaction.md) — The Manage-sessions section describes Claude automatically summarizing the conversation when context fills and `/compact` to trigger it earlier — the compaction mechanism this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The tasks pane shows the subagents (alongside background commands and dynamic workflows) running inside a session — the subagent execution this term defines, here in the desktop GUI.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The note's prompt box pulls in @mention files and attachments as context and sessions persist their own history — the per-session state/memory this term covers.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Starting a session requires choosing a permission mode and the prompt box supports interrupt/steer mid-action — the graduated-trust control loop this term defines.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — Parallel sessions (each in its own Git worktree) and side chats let multiple Claude instances work without interfering — the multiple-coordinating-agents pattern this term defines.

### 8. `cc_desktop_permission_modes` (6 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — This note IS the desktop permission-mode ladder (Ask permissions → Auto accept edits → Plan → Auto → Bypass) — the graduated-trust escalation model this term defines, presented as the GUI mode selector.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The five modes, their settings keys, and the `dontAsk` CLI-only note are Claude Code's own permission system, so the product term anchors the feature.
- [Deny-First](../../term_dictionary/term_deny_first.md) — Bypass permissions still honors explicit ask rules and Auto mode runs background safety checks — the deny/ask-rules-take-precedence behavior this term defines even when prompts are skipped.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The note states Bypass permissions should only be used in sandboxed containers/VMs and that cloud sessions omit Bypass because the environment is already sandboxed — the sandbox isolation boundary this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Auto mode executes all actions with background alignment checks to reduce prompts while keeping oversight — the autonomous-but-supervised operating mode this term defines.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — Plan mode has Claude reason through and propose an approach without editing source, an explicit-reasoning-before-acting step the chain-of-thought term covers.

### 9. `cc_desktop_diff_review_and_pr` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the Claude Desktop verify-review-PR loop (preview, diff view, self-review, CI monitoring), so the product term anchors the surface whose review workflow it describes.
- [Diff](../../term_dictionary/term_diff.md) — The note centers on the diff view — file-by-file added/removed lines, the `+12 -1` indicator, inline line comments — the code-diff representation this term defines.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — PR monitoring polls CI check results with auto-fix and auto-merge once checks pass — the continuous-integration pipeline this term defines, here driven from the desktop.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Diff review with accept/reject/comment, and the opt-in auto-fix/auto-merge toggles, are graduated-trust gates over how much of the PR flow runs unattended — the escalation model this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Auto-verify takes screenshots, inspects the DOM, clicks elements, and fixes issues it finds after every edit — the self-verifying autonomous-agent behavior this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — App preview and auto-verify rely on Claude calling browser/server tools (screenshots, endpoint tests, log inspection), and `.claude/launch.json` configures the dev-server tool — the tool-use mechanism this term defines.

### 10. `cc_desktop_workspace_panes` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the Claude Desktop workspace (pane layout, terminal, file editor, view modes, shortcuts) and computer use, so the product term anchors the surface whose UI it describes.
- [Diff](../../term_dictionary/term_diff.md) — The pane layout includes a dedicated diff pane and a `Cmd+Shift+D` toggle, and clicking a diff path opens the file pane — the diff-view UI this term grounds.
- [Context Window](../../term_dictionary/term_context_window.md) — The usage ring shows per-session context window usage versus plan usage — the context-window measurement this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The subagent pane and tasks pane display subagent output and let you stop a running subagent — the subagent execution this term defines, visible in the desktop layout.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Computer use is a coarse tool category that Claude falls back to after connector/Bash/Chrome tools, with per-app access tiers — the tool-selection-and-use behavior this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Computer use is off by default, requires explicit enabling plus macOS Accessibility/Screen-Recording grants, and prompts per-app with fixed view-only/click-only/full-control tiers — the graduated-trust gating this term defines.
- [Automation](../../term_dictionary/term_automation.md) — Computer use lets Claude drive native apps, GUIs, and mobile simulators that lack a CLI — the GUI-automation capability this term defines.

### 11. `cc_desktop_environments_extend_and_enterprise` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Desktop's environment config, extension surfaces, enterprise controls, and the desktop↔CLI shared-config contract, so the product term anchors all of them.
- [SSH](../../term_dictionary/term_ssh.md) — The note details SSH sessions (host/port/identity-file dialog, remote auto-install) plus the managed `sshConfigs`/`sshHostAllowlist` keys — the SSH remote-execution and host-restriction mechanics this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Connectors are described as MCP servers with a graphical setup flow, and `managedMcpServers` pushes MCP configs to all users — the MCP server model this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The Extend section's "Use skills" subsection invokes built-in/custom/project/plugin skills from the prompt box — the skills mechanism this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Enterprise managed settings (`disableBypassPermissionsMode`, `disableAutoMode`, `autoMode` classifier) constrain which permission modes users may enable — the graduated-trust governance this term covers.
- [Context Window](../../term_dictionary/term_context_window.md) — Cloud sessions support multiple repositories and continue running while the app is closed, each session carrying its own context — the per-session context window this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Remote/cloud sessions run long-running refactors/tests/migrations that continue even if you close the app, and Dispatch spawns Code sessions on its own — the autonomous-agent operating modes this term defines.

> **Sibling `cc_*` cross-links (added in each note's `## Related Notes`, after term notes):** notes 1–4 cross-link
> each other (the VS Code cluster); notes 6–11 cross-link each other (the Desktop cluster); note 5 links the
> VS Code cluster (sibling IDE surface); all 11 link `cc_platforms_and_integrations` (B01A, the surface
> comparison hub). Cross-sub-plan link-outs (B05A/B05B/B06/B08A/B09A/B10B/B11/B12B/B13A/B14A/B14B/B16/B17) are
> prose references, not counted toward the ≥6 term-note minimum.

## Section Coverage Map

Every source H2/H3 maps to a note OR an explicit link-out (sections owned by other sub-plans are LINKED, not duplicated).

```
vs-code.md
├── Prerequisites ───────────────────────── → note 1 (cc_vs_code_extension)
├── Install the extension ───────────────── → note 1
├── Get started (4 Steps) ───────────────── → note 1
│   └── permission modes intro ──────────── → note 1 (summary) → linked out B05A
├── Use the prompt box (+4 H3) ──────────── → note 2 (cc_vs_code_prompt_box_and_sessions)
│   └── extended thinking ───────────────── → note 2 → link term_chain_of_thought / B03B model-config
├── Customize your workflow (+3 H3) ─────── → note 2
├── Manage plugins (+2 H3) ──────────────── → note 2 (UI) → concept link-out B09A plugins
├── Automate browser tasks with Chrome ──── → note 2 (UI) → linked out B13A chrome.md
├── VS Code commands and shortcuts (+H3) ── → note 3 (cc_vs_code_settings_and_cli_relationship)
├── Configure settings (+Extension table) ─ → note 3
├── VS Code extension vs. Claude Code CLI ─ → note 3
│   └── Rewind with checkpoints ─────────── → note 3 → concept link-out B02B checkpointing.md
├── Work with git (+2 H3) ───────────────── → note 3 → worktree concept link-out B10B worktrees.md
├── Use third-party providers ───────────── → note 3 (summary) → linked out B14A
├── Security and privacy ────────────────── → note 4 (intro) / note 1 (restricted-mode fix)
│   └── The built-in IDE MCP server ─────── → note 4 (cc_vs_code_ide_mcp_server)
├── Fix common issues (+4 H3) ───────────── → note 1
├── Uninstall the extension ─────────────── → note 1
└── Next steps ──────────────────────────── → note 1 (links)
jetbrains.md
├── Supported IDEs ──────────────────────── → note 5 (cc_jetbrains_plugin)
├── Features ────────────────────────────── → note 5
├── Installation ────────────────────────── → note 5
├── Usage (+2 H3) ───────────────────────── → note 5
├── Configuration (+2 H3) ───────────────── → note 5
├── Special configurations (+2 H3) ──────── → note 5 (remote dev + WSL2 fixes)
├── Troubleshooting (+3 H3) ─────────────── → note 5
└── Security considerations ─────────────── → note 5 → permission concept link-out B05A
desktop.md
├── (intro: three tabs, session model) ──── → note 7 (cc_desktop_overview_and_sessions)
├── Start a session ─────────────────────── → note 7
├── Work with code ──────────────────────── →
│   ├── Use the prompt box ───────────────── → note 7
│   ├── Add files and context ────────────── → note 7
│   ├── Choose a permission mode ─────────── → note 8 (cc_desktop_permission_modes) → concept B05A
│   ├── Preview your app ─────────────────── → note 9 (cc_desktop_diff_review_and_pr)
│   ├── Review changes with diff view ────── → note 9
│   ├── Review your code ─────────────────── → note 9
│   └── Monitor pull request status ──────── → note 9
├── Arrange your workspace ──────────────── →
│   ├── Run commands in the terminal ─────── → note 10 (cc_desktop_workspace_panes)
│   ├── Open and edit files ──────────────── → note 10
│   ├── Open files in other apps ─────────── → note 10
│   ├── Switch view modes ────────────────── → note 10
│   ├── Keyboard shortcuts ───────────────── → note 10
│   └── Check usage ──────────────────────── → note 10
├── Let Claude use your computer (+3 H3) ── → note 10 → depth link-out B13A computer-use.md
├── Manage sessions ─────────────────────── →
│   ├── Work in parallel with sessions ───── → note 7 → worktree concept B10B worktrees.md
│   ├── Ask a side question ──────────────── → note 7
│   ├── Watch background tasks ───────────── → note 7 → dynamic workflows B10B workflows.md
│   ├── Run long-running tasks remotely ──── → note 11 → cloud/web link-out B12B
│   ├── Continue in another surface ──────── → note 11
│   └── Sessions from Dispatch ───────────── → note 11 → Dispatch/RemoteControl link-out B12B/B11
├── Extend Claude Code ──────────────────── →
│   ├── Connect external tools ───────────── → note 11 → MCP concept B08A mcp.md
│   ├── Use skills ───────────────────────── → note 11 → skills concept B06 skills.md
│   ├── Install plugins ──────────────────── → note 11 → plugins concept B09A plugins.md
│   └── Configure preview servers (+4 H3) ── → note 9 (launch.json owner)
├── Environment configuration (+3 H3) ───── → note 11 (Local/Cloud/SSH)
├── Enterprise configuration (+6 H3) ────── → note 11 → auth/network/managed-settings depth B14B; data B16
├── Coming from the CLI? (+4 H3) ────────── → note 11 (shared config, flag/feature tables, what's not avail)
└── Troubleshooting (+9 H3) ─────────────── → note 11 (desktop-specific) → API errors link-out B17 errors.md
desktop-quickstart.md
├── (intro: Chat/Cowork/Code tabs) ──────── → note 6 (cc_desktop_quickstart)
├── Install (2 Steps) ───────────────────── → note 6
├── Start your first session (4 Steps) ──── → note 6
├── Now what? ───────────────────────────── → note 6 (try-next tour → links into notes 7–11)
├── Coming from the CLI? ────────────────── → note 6 → full comparison in note 11
└── What's next ─────────────────────────── → note 6 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| desktop.md (8,626w, ~11 H2 / 26 H3) | notes 6–11 (6 notes) + many link-outs | far over the 2,500-word cap; distinct operating concerns differ in BB (permission modes = concept; diff/review = procedure) and topic (sessions vs panes vs computer use vs environments/enterprise). quickstart split off as note 6. |
| vs-code.md (5,344w, 12 H2 / 13 H3) | notes 1–4 (4 notes) | over the cap; setup+fixes (note 1) vs prompt-box+sessions (note 2) vs settings+CLI-relationship+git (note 3) vs the IDE MCP server (note 4, the one *concept* on the page) differ in scope/BB. |
| jetbrains.md (1,185w) | note 5 (whole page) | under the cap; single coherent surface — kept as one procedure note. |
| desktop-quickstart.md (1,376w) | note 6 (whole page) | under the cap; single getting-started procedure. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_vs_code_extension | procedure | 700 | 2 | ✅ (uninstall rm -rf examples; cap 6) |
| 2 | cc_vs_code_prompt_box_and_sessions | procedure | 650 | 2 | ✅ (@-mention + @browser examples) |
| 3 | cc_vs_code_settings_and_cli_relationship | procedure | 750 | 4 | ✅ (mcp add, worktree, vscode:// URI, git examples) |
| 4 | cc_vs_code_ide_mcp_server | concept | 450 | 0 | ✅ (tables only) |
| 5 | cc_jetbrains_plugin | procedure | 600 | 4 | ✅ (/ide, hostname -I, firewall rule, .wslconfig) |
| 6 | cc_desktop_quickstart | procedure | 650 | 0 | ✅ (no code) |
| 7 | cc_desktop_overview_and_sessions | procedure | 700 | 0 | ✅ (prose/UI) |
| 8 | cc_desktop_permission_modes | concept | 450 | 0 | ✅ (mode table) |
| 9 | cc_desktop_diff_review_and_pr | procedure | 750 | 3 | ✅ (launch.json — trimmed to 3 representative configs to stay ≤6) |
| 10 | cc_desktop_workspace_panes | procedure | 700 | 0 | ✅ (shortcut/tier tables) |
| 11 | cc_desktop_environments_extend_and_enterprise | procedure | 800 | 4 | ✅ (sshConfigs, sshHostAllowlist, git fetch, managed-settings examples) |

No note exceeds the caps (≤400 lines / ≤2500 words / ≤6 code). Note 9 is the only code-dense note — `desktop.md`
has 4 `launch.json` JSON blocks plus the auto-verify block; the plan trims to **3 representative configurations**
(single-server, multiple-servers, node-script) to stay within the 6-code-block cap while preserving every field
documented in the configuration-fields table. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_vs_code_extension cc_vs_code_prompt_box_and_sessions cc_vs_code_settings_and_cli_relationship cc_vs_code_ide_mcp_server cc_jetbrains_plugin cc_desktop_quickstart cc_desktop_overview_and_sessions cc_desktop_permission_modes cc_desktop_diff_review_and_pr cc_desktop_workspace_panes cc_desktop_environments_extend_and_enterprise"
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

Single phase (11 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 11 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 11 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB in-degree ≥1 confirmed for all 11 after inlinks added | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 11 rows** under a "Surfaces — IDE & Desktop" cluster + increments the
BB-distribution counts (procedure ×9, concept ×2). The entry-point back-link is added to each note at finalization.

## Undigested Terms Plan (Step 4e)

b12a creates **0 new `term_dictionary` captures**. Step 2d re-scan of all 4 pages (emphasis/tables/captions)
surfaced surface-feature vocabulary, each routed to an existing term note or its home sub-plan (Pattern B,
dedup across term_dictionary AND documentation/):

| Term surfaced (page) | Disposition |
|---|---|
| Spark icon / Editor Toolbar / Activity Bar (vs-code) | UI detail folded into note 1 (no term note) |
| `ide` MCP server / `mcp__ide__getDiagnostics` / `mcp__ide__executeCode` (vs-code) | folded into note 4; concept = `term_mcp` (link, exists) |
| Checkpoints / Rewind / Fork (vs-code, desktop) | link `term_agentic_memory` (note 3/7) + concept link-out B02B `checkpointing.md` |
| Permission mode / Plan mode / Auto mode / Bypass (desktop) | note 8 + link `term_graduated_trust` (exists); concept owner B05A |
| Git worktree / parallel sessions (desktop) | note 7 + concept link-out B10B `worktrees.md`; no new term |
| Computer use / app-access tiers (desktop) | note 10 + link `term_automation` (exists); depth owner B13A `computer-use.md` |
| Connector (desktop) | folded into note 11; concept = `term_mcp` (connectors are MCP-with-GUI; link, exists) |
| Dispatch / Cowork / Remote / SSH session (desktop) | note 11; SSH = `term_ssh` (link, exists); Dispatch/Remote surface comparison owned by B12B |
| Side chat (`/btw`) / view modes / preview server / launch.json (desktop) | folded into notes 7/9/10 (UI features, no term notes) |
| Managed settings / `sshHostAllowlist` / MDM (desktop) | folded into note 11; depth owner B14B `server-managed-settings.md` |
| WSL2 / mirrored networking (jetbrains) | folded into note 5 (config detail, no term note) |

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B12A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the surface concepts duplicate existing notes?) was
performed: `term_claude_code`, `term_vscode`, `term_cursor`, `term_cline`, `term_mcp`, `term_subagent`,
`term_context_window`, `term_compaction`, `term_sandbox`, `term_skills`, `term_graduated_trust`,
`term_autonomous_coding_agents`, `term_ssh`, `term_diff`, `term_ci_cd`, `term_function_calling`,
`term_agentic_memory`, `term_deny_first`, `term_multi_agent`, `term_automation`, `term_ai_assisted_development`,
`term_chain_of_thought` all exist → linked, not recreated. **0 new B12A `term_dictionary` captures.**

## Term-Note Authoring Requirements

**N/A for b12a** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (bash/JSON/text examples copied exactly from the source). One BB per note. Each note
  ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8, in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_vscode.md` | notes 1, 2, 3, 4 | VS Code term → the VS Code extension surface cluster |
| `term_dictionary/term_cursor.md` | note 1 | Cursor term → extension installs into Cursor (a VS Code fork) |
| `term_dictionary/term_claude_code.md` | notes 6, 7, 11 | product term → desktop getting-started / operating reference / shared-config |
| `term_dictionary/term_ssh.md` | note 11 | SSH term → desktop SSH-session configuration |
| `term_dictionary/term_graduated_trust.md` | note 8 | permission-mode term → desktop permission modes |
| `term_dictionary/term_ci_cd.md` | note 9 | CI/CD term → desktop PR monitoring (auto-fix/auto-merge) |
| `term_dictionary/term_automation.md` | note 10 | automation term → desktop computer use (GUI automation) |
| `cc_jetbrains_plugin` is reached via | `term_dictionary/term_claude_code.md` | product term → JetBrains plugin surface (note 5 inbound) |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | notes 1, 6 | getting-started tutorial → VS Code + desktop quickstart |

## Follow-up Recommendations

- After the 11 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 11
  rows for `entry_claude_code_docs.md` under the "Surfaces — IDE & Desktop" cluster; `/tessellum-check-broken-links`.
- Cross-link to B12B (web/remote surfaces) once it executes, so the full surface comparison (CLI/IDE/Desktop/
  Web/Mobile/Remote-Control/Dispatch) is reciprocally connected from `cc_platforms_and_integrations` (B01A).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B12A, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/`; measured words match
  the master's B12A figure (vs-code 5,344 · jetbrains 1,185 · desktop 8,626 · desktop-quickstart 1,376 = 16,531).
  `desktop.md` confirmed as the corpus's largest page — forced the 6-way split (notes 6–11).
- **Notes**: 11 (procedure 9, concept 2) — matches master estimate. Splits documented in Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–7 term notes per note (22 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
  cross-links and cross-sub-plan link-outs kept as prose, not counted toward the minimum.
- **Dedup (G-B, across term_dictionary AND documentation/)**: confirmed no existing `cc_` notes and no
  22 existing terms linked, not recreated.
- **Step 2d new-term scan**: surface-feature vocabulary surfaced (Spark icon, IDE MCP server, connectors,
  Dispatch, SSH session, computer use, managed settings) — all routed to existing term notes / home sub-plans;
  **0 new B12A term captures**.
- **Sections present**: Scope, Content Strategy, Source Pages (measured), Planned Notes (LOCKED), Summary
  Statistics & BB Distribution, Per-Note Related Notes Mapping (LOCKED), Section Coverage Map, Split Decisions,
  Density Re-Assessment (LOCKED), Validation Scripts, Per-Phase Validation Gate (G1–G8 incl G7/G8), Entry Point
  Decision, Undigested Terms Plan, Term-Note Authoring Requirements, Pacing Rules, Inlinks, Follow-up
  Recommendations, Pipeline Status, Augmentation Report, Review Sign-Off.
- **28-item checklist**: PASS (term-note items N/A — B12A authors no terms; entry-point + undigested-terms
  inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8 incl G7/G8) | ✅ PASS | 8 gate rows present (single phase); G7/G8 Discoverability (inbound in-degree ≥1) included with executed Inlinks table. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B12A contributes 11 rows under "Surfaces — IDE & Desktop". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 11 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | Largest note 800w / 4 code (note 11) — well under caps; note 9 code-density resolved by trimming launch.json to 3 representative configs. None borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w`: vs-code 5,344 · jetbrains 1,185 · desktop 8,626 · desktop-quickstart 1,376 = 16,531 = master B12A figure. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B12A authors 0 term notes; Undigested Terms Plan routes all surfaced terms (Pattern B, dedup across term_dictionary AND documentation/); Authoring Requirements inherited. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
