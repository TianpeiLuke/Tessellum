---
title: Sub-Plan B12B — Claude Code Docs: Web & Remote Surfaces
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["claude-code-on-the-web", "web-quickstart", "remote-control", "deep-links"]
---

# Sub-Plan B12B: Web & Remote Surfaces

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 pages that document where Claude Code runs **away from the local terminal**: in Anthropic's managed
cloud (Claude Code on the web + its quickstart), driven from another device against your own machine
(Remote Control), and launched from a clickable URL (deep links). P2 (Phase B) — these surfaces build on
P1 cores (sessions, permissions, sandboxing, MCP, hooks, context window) which are linked, not duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 13,671 measured words. **Planned: 10 notes.**

## Content Strategy

- **Prioritize**: the cloud-environment model (fresh VM, what carries over, network access levels/proxies)
  and the cross-surface comparison (web vs Remote Control vs CLI vs Desktop) — the load-bearing decisions a
  team makes when adopting these surfaces.
- **Group**: split the 6.3Kw `claude-code-on-the-web` (11 H2, 26 H3) by concept vs procedure — cloud
  environment / network model (concept) vs setup scripts / move-tasks / session-management (procedure) vs
  security-isolation (concept). Keep `web-quickstart` as one onboarding procedure. Keep `remote-control`
  as a setup procedure + a surface-comparison concept. Keep `deep-links` as a concept + a build procedure.
- **Skip / link-out (own other sub-plans)**: sessions → B02B (sessions.md); context-window/compaction →
  B02A; sandboxing → B05B; permission modes/plan mode → B05A; hooks/SessionStart → B07A/B07B; MCP → B08A;
  subagents/agent-teams → B10A; worktrees → B10B; routines/scheduled-tasks → B11; ultraplan/ultrareview/
  code-review/GitHub Enterprise → B13B; Slack → B13A; Desktop/Dispatch/VS Code → B12A; CLI reference →
  B03B; env-vars/settings/managed-settings → B03A/B14B; authentication → B14B; security/data-usage/ZDR →
  B16; errors → B17. These are referenced via links, never duplicated.
- **Terms**: no new `term_dictionary` captures — vocabulary routes to existing term notes (Pattern B; see
  Undigested Terms Plan). Master owns "Remote Control / Teleport" as **doc-concept owner → B12B** (these
  are digested as `cc_` doc notes here, not as term notes).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| claude-code-on-the-web | /claude-code-on-the-web | 6,326 | 13 | 11 | 26 | concept + procedure |
| web-quickstart | /web-quickstart | 2,497 | 1 | 8 | 9 | procedure |
| remote-control | /remote-control | 2,973 | 4 | 9 | 8 | procedure + concept |
| deep-links | /deep-links | 1,875 | 6 | 7 | 8 | concept + procedure |

> Code/H2/H3 counts include code fences and headings nested inside MDX `<Steps>` / `<Tabs>` / `<Accordion>`
> blocks. The "default allowed domains" AccordionGroup in `claude-code-on-the-web` is one large reference
> table, not free prose. In `deep-links` the `## High 5xx rate on web-gateway` heading at L106 is **content
> inside a sample runbook code block**, not a real source H2 (so 7 true H2, not 8).

> **H2 lists (document order):**
> - **claude-code-on-the-web**: GitHub authentication options · The cloud environment (H3 What's available · Installed tools · Work with GitHub issues and PRs · Link artifacts back to the session · Run tests/start services/add packages · Resource limits · Configure your environment) · Setup scripts (H3 Environment caching · Setup scripts vs SessionStart hooks · Install dependencies with a SessionStart hook) · Network access (H3 Access levels · Allow specific domains · GitHub proxy · Security proxy · Default allowed domains) · Move tasks between web and terminal (H3 From terminal to web [H4 Tips · Send local repos without GitHub] · From web to terminal [H4 Teleport requirements · `--teleport` is unavailable]) · Work with sessions (H3 Manage context · Review changes · Share sessions [H4 Enterprise/Team · Max/Pro] · Archive · Delete) · Auto-fix pull requests (H3 How Claude responds to PR activity) · Security and isolation · Troubleshooting (H3 Session creation failed · Remote Control session expired · Environment expired) · Limitations · Related resources
> - **web-quickstart**: How sessions run · Compare ways to run Claude Code · Connect GitHub and create an environment (H3 Connect from your terminal) · Start a task · Pre-fill sessions · Review and iterate · Troubleshoot setup (H3 No repos appear · GitHub login button · Not available for org · `/web-setup` Unknown command · Could not create env · Setup script failed · Sessions hang/time out · Session keeps running) · Next steps
> - **remote-control**: Requirements · Start a Remote Control session (H3 Connect from another device · Enable Remote Control for all sessions) · Connection and security · Remote Control vs Claude Code on the web · Mobile push notifications · Limitations · Troubleshooting (H3 6 named errors) · Choose the right approach · Related resources
> - **deep-links**: How it works (H3 What a launched session shows) · Build a link (H3 Choose between `cwd` and `repo`) · Examples (H3 Embed a link in a runbook · Open a link from the shell) · Registration and supported platforms · Open a VS Code tab instead of a terminal · Troubleshooting (H3 4 named issues) · Learn more

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **10 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_web_overview.md` | concept | on-the-web: intro, page-map; web-quickstart: intro, How sessions run | 450 | What Claude Code on the web is (managed cloud VM at claude.ai/code, persists across devices, mobile-monitorable); the clone→configure→work→push lifecycle; what it's good for; research-preview/plan availability. |
| 2 | `cc_web_quickstart.md` | procedure | web-quickstart: Connect GitHub & create env (+ Connect from terminal), Start a task, Review and iterate | 600 | Onboarding procedure: connect GitHub App (or `/web-setup` from terminal), create a cloud environment, select repo/branch + permission mode, submit a task, open diff / leave inline comments / create PR / iterate. |
| 3 | `cc_cloud_environment.md` | concept | on-the-web: The cloud environment (What's available, Installed tools, GH issues/PRs tools, link artifacts, run tests/services, Resource limits, Configure env) | 650 | The fresh per-session VM: carries-over table (repo `.claude/` yes vs user/local no), pre-installed runtimes/tools, built-in GitHub tools, `CLAUDE_CODE_REMOTE_SESSION_ID` link-back, resource ceilings, environment configuration (vars, `/remote-env` default). |
| 4 | `cc_web_setup_scripts.md` | procedure | on-the-web: Setup scripts (Environment caching, Setup scripts vs SessionStart hooks, Install deps with SessionStart hook) | 550 | Setup-script authoring (Bash, runs as root pre-launch, <5 min budget, `\|\| true`); environment caching/snapshot semantics; setup-script vs repo SessionStart hook decision; `CLAUDE_CODE_REMOTE` guard. |
| 5 | `cc_cloud_network_access.md` | concept | on-the-web: Network access (Access levels, Allow specific domains, GitHub proxy, Security proxy, Default allowed domains) | 550 | Outbound-access model: None/Trusted/Full/Custom levels; custom allowlists with wildcards; the GitHub proxy (scoped credential, push-to-branch restriction) vs the security proxy (filtering/audit); the Trusted default-domain allowlist (registries/VCS/registries by category). |
| 6 | `cc_move_tasks_web_terminal.md` | procedure | on-the-web: Move tasks between web and terminal (From terminal to web + tips + send local repos; From web to terminal + teleport requirements + unavailable) | 600 | `--remote` (new cloud session, clones GitHub remote) vs `--teleport`/`/teleport`/`/tasks`→`t` (pull cloud session local); plan-locally/execute-remotely + parallel patterns; `CCR_FORCE_BUNDLE` local bundling; teleport requirements; `--remote` vs `--remote-control` vs `--resume` disambiguation. |
| 7 | `cc_web_session_management.md` | procedure | on-the-web: Work with sessions (Manage context, Review changes, Share sessions, Archive, Delete), Auto-fix pull requests | 600 | Cloud-session lifecycle: text-output commands (`/compact`,`/context`; not `/clear`,`/model`); review/inline comments; share visibility (Team vs Public, repo-access verification); archive/delete; Auto-fix PRs (subscribe to CI/review events, clear vs ambiguous fixes, GitHub App requirement, comment-automation warning). |
| 8 | `cc_web_security_and_limits.md` | concept | on-the-web: GitHub authentication options, Security and isolation, Limitations, Troubleshooting; web-quickstart: Troubleshoot setup | 550 | Isolation model (per-session VM, network controls, credential protection via proxy); GitHub-App-vs-`/web-setup` auth and its access-scope caveat; rate-limit/platform/IP-allowlist/ZDR limitations; cloud-session troubleshooting (creation failed, env expired, setup-script failures). |
| 9 | `cc_remote_control.md` | procedure | remote-control: intro, Requirements, Start a session (server/interactive/from-session/VS Code), Connect from another device, Enable for all, Connection and security, Mobile push, Limitations, Troubleshooting | 750 | Drive a local session from phone/browser: requirements; the four start modes (`claude remote-control` server + flags, `--remote-control`/`--rc`, `/remote-control`, VS Code); connect via URL/QR/session-list; enable-for-all `/config`; outbound-only HTTPS + short-lived credentials; mobile push setup; limitations + named eligibility errors. |
| 10 | `cc_remote_vs_web_and_deep_links.md` | concept | remote-control: Remote Control vs web, Choose the right approach; deep-links: full page (How it works, Build a link, Examples, Registration, VS Code tab, Troubleshooting) | 600 | Two cross-surface decision aids: (a) Remote Control (local exec) vs web (cloud exec) and the away-from-terminal matrix (Dispatch/Remote Control/Channels/Slack/Scheduled); (b) `claude-cli://open` deep links — `q`/`cwd`/`repo` params, inert-until-Enter safety, OS handler registration, GitHub-strips-scheme caveat. |

**Estimate: 10 notes** — concept ×5 (notes 1,3,5,8,10), procedure ×5 (notes 2,4,6,7,9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (13,671 words). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,900 (avg ~590/note). Code blocks: ≤2 per note (verbatim Bash/JSON/URL snippets where load-bearing); the source's 13 web-page fences are mostly small Bash/`.env`/URL examples + one large domain-allowlist accordion (rendered as a reference table, not a code block).
- **Building Block Distribution**: concept ×5 (notes 1,3,5,8,10) · procedure ×5 (notes 2,4,6,7,9). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_web_overview` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the identity page for a Claude Code surface (the web/cloud one), so the product term is its definitional anchor.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note frames the web surface around "tasks that don't need frequent steering": submit a well-defined task and review when done — the autonomous operating mode this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note stresses Claude Code "behaves the same everywhere"; the web surface is the same harness runtime presented on cloud infra instead of the local terminal.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The note's core claim is that each session runs in an isolated Anthropic-managed VM, i.e. a cloud sandbox separating the agent from your machine.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The clone→work→push lifecycle ends each work increment by pushing a branch for review, the durable-checkpoint discipline this term describes applied to cloud runs.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — A headline benefit is running several independent tasks at once, each in its own session and branch — the parallel-agents pattern this term covers.

### 2. `cc_web_quickstart` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This is the onboarding procedure for a Claude Code surface, so the product term grounds every step (GitHub connect, environment, task submit).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — Connecting GitHub via the App or `/web-setup` (syncing the local `gh` token to your Claude account) is an OAuth/token-grant flow, the credential mechanism this term explains.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — A quickstart step is choosing a permission mode (Accept edits vs Plan; cloud omits Ask/Bypass), the progressive-trust ladder this term defines.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The review-and-iterate loop (open diff, inline comments, create PR, keep going) is the checkpoint-review cadence this term describes, applied to a cloud branch.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The "Be specific / name the file" task-description guidance is exactly how you brief an autonomous coding agent for an unattended run, the category this term defines.
- [Sandbox](../../term_dictionary/term_sandbox.md) — Step 1 clones the repo into an isolated VM where Claude works before pushing; the quickstart is the user-facing entry into that cloud sandbox.

### 3. `cc_cloud_environment` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — The note describes the fresh per-session VM (what's available, pre-installed tools, resource ceilings) — the concrete cloud sandbox each session runs in.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The carries-over table is defined entirely in Claude Code terms (repo `CLAUDE.md`, `.claude/settings.json`, `.mcp.json`, skills/agents/commands), so the product term anchors what "available in cloud sessions" means.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The note explains the repo's `CLAUDE.md` carries over but user `~/.claude/CLAUDE.md` does not — the persistent-instruction memory mechanism this term covers, scoped to the clone.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note's availability table calls out that `.mcp.json` MCP servers carry over but `claude mcp add` user-config servers do not, so MCP configuration is central to environment portability.
- [Skills](../../term_dictionary/term_skills.md) — The note distinguishes repo `.claude/skills/` (available) from user skills (not, except claude.ai-enabled), making skill loading a key cloud-environment behavior.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — The note explains there is no secrets store yet and that interactive auth like AWS SSO can't run in a cloud VM (it needs browser login), the token/credential constraints this term frames.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note documents how the harness's execution environment is provisioned in the cloud (runtimes, GitHub tools, env vars), the runtime-context layer this term defines.

### 4. `cc_web_setup_scripts` (6 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — Setup scripts customize the cloud sandbox before launch (install deps, configure tools); the note is about provisioning that isolated VM.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Setup scripts and SessionStart hooks are Claude Code configuration surfaces (`.claude/settings.json`, env UI), so the product term grounds where each lives.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Environment caching snapshots the post-setup filesystem and reuses it as a starting point for later sessions — a checkpoint/snapshot of the prepared environment, the durable-state idea this term covers.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Choosing what runs at session start (setup script for cloud-only toolchain vs SessionStart hook for cloud+local project setup) is deliberate session-start environment shaping, the engineering discipline this term names.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Setup scripts and the cache feed the same environment whose MCP servers (declared in `.mcp.json`) load at session start, tying provisioning to MCP availability.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The note shows persisting environment variables for later Bash commands via `$CLAUDE_ENV_FILE`, a session-scoped state-persistence mechanism analogous to the memory concept this term defines.

### 5. `cc_cloud_network_access` (6 term notes)
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — The note centers on the GitHub proxy and security proxy that sit between the sandbox and the internet, intercepting/translating all outbound traffic — the intermediary-server role this term defines.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — The GitHub proxy interposes a scoped credential and translates it to the real GitHub token (a protection/remote proxy that controls access), the surrogate-access pattern this term formalizes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — Network access levels (None/Trusted/Full/Custom) are the cloud sandbox's outbound-isolation controls; the note is about how tightly the VM is sealed.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The default Trusted allowlist and per-environment configuration are Claude Code on the web settings, so the product term anchors what these controls govern.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — The security proxy provides content filtering and a DNS-level audit trail over TLS-bound traffic; pinning is the adjacent transport-trust control this term explains, relevant to evaluating proxy-mediated HTTPS.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note notes MCP connector traffic is routed through Anthropic's servers so connectors work without adding hosts to Allowed domains — an MCP-specific exception to the network model this note documents.

### 6. `cc_move_tasks_web_terminal` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code CLI flags/commands (`--remote`, `--teleport`, `/teleport`, `/tasks`) for moving work between surfaces, so the product term anchors the commands.
- [Sandbox](../../term_dictionary/term_sandbox.md) — `--remote` spins up a fresh cloud sandbox that clones your GitHub remote; the note is about creating and pulling from that isolated VM.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The note's hard rule "push first, the VM clones from GitHub not your machine" and teleport's clean-git-state requirement make committed checkpoints the unit of handoff, the discipline this term covers.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — "Run tasks in parallel" — each `--remote` creates its own independent cloud session running simultaneously — is the parallel-agents pattern this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The plan-locally/execute-remotely pattern uses `--permission-mode plan` to draft safely, then hands an autonomous cloud run the trust to execute — the trust-escalation ladder this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Teleporting/`--remote` send a well-scoped task to run autonomously in the cloud while you work locally, the unattended-agent mode this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — Teleport loads the full cloud conversation history into your terminal; the moved session carries its accumulated context across surfaces, the working-memory container this term defines.

### 7. `cc_web_session_management` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note covers which Claude Code built-in commands work in cloud sessions and the session sidebar lifecycle, so the product term anchors the command/UI surface.
- [Compaction](../../term_dictionary/term_compaction.md) — A dedicated "Manage context" subsection covers `/compact` (with focus) and auto-compaction overrides (`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`) in cloud sessions, the context-summarization mechanism this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — `/context` shows what's in the window and auto-compaction triggers as the window fills; the note's context-management commands all operate on the window this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The note states subagents work the same in cloud sessions (spawned via the Task tool into a separate context window, picked up from `.claude/agents/`), the delegation mechanism this term covers.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Reviewing diffs, creating PRs, and Auto-fix watching the PR are checkpoint-and-review steps on the pushed branch, the cadence this term describes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Auto-fix has Claude autonomously watch a PR and push fixes for CI failures and review comments — unattended agentic behavior, the category this term defines.

### 8. `cc_web_security_and_limits` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — The Security and isolation section enumerates the per-session isolated VM, network controls, and credential protection — the sandbox isolation guarantees this term defines.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — GitHub authentication options (App authorization vs `/web-setup` syncing the `gh` token) and the access-scope caveat are token-grant mechanics, the credential model this term explains.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — Credential protection works because authentication is handled through a secure proxy using scoped credentials so secrets never enter the sandbox — the intermediary-server role this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The limitations (shared rate limits, GitHub-only cloning, IP-allowlist incompatibility) and troubleshooting are Claude Code on the web constraints, so the product term anchors them.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — The scoped-credential proxy that verifies and translates to your real token is a protection proxy controlling access on the agent's behalf, the surrogate-access pattern this term formalizes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — App installation is explicitly "not a session-level access control"; the note tells you to restrict at GitHub and choose permission posture deliberately — the trust-scoping discipline this term covers.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — The isolation layers (isolated VMs, secure analysis before PR creation) describe the managed backend that hosts each cloud session, the infrastructure layer this term names.

### 9. `cc_remote_control` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's Remote Control commands/flags (`claude remote-control`, `--remote-control`/`--rc`, `/remote-control`, VS Code `/rc`), so the product term anchors them.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Remote Control keeps the full local harness running (filesystem, MCP servers, tools, project config) and just exposes it to remote devices — the local runtime this term defines.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Remote Control survives interruptions (laptop sleep, network drop) by reconnecting when the machine returns, keeping a durable in-progress session — the resilience this term's snapshot/recovery idea covers.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — Multiple troubleshooting errors hinge on full-scope claude.ai OAuth vs inference-only `setup-token`/`CLAUDE_CODE_OAUTH_TOKEN`; the note's auth requirements are exactly the token-scope distinctions this term explains.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — Connection-and-security: outbound-only HTTPS over TLS with multiple short-lived, single-purpose credentials — the transport-trust regime this term's pinning control is part of.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — A headline Remote Control benefit is that your local MCP servers stay available remotely; `/mcp` even works from mobile/web as a text summary, making MCP central to the surface.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Remote Control is admin-gated (off by default on Team/Enterprise, `disableRemoteControl` managed setting, workspace-trust dialog), the layered-trust/permission posture this term defines.

### 10. `cc_remote_vs_web_and_deep_links` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note compares Claude Code surfaces and documents the `claude-cli://` deep-link scheme, so the product term anchors both decision aids.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The Remote-Control-vs-web axis is fundamentally "where the harness runs" — your machine vs Anthropic cloud — the runtime this term defines.
- [Sandbox](../../term_dictionary/term_sandbox.md) — One side of the comparison (web) runs in a cloud sandbox while Remote Control runs on your machine; the matrix is largely about that isolation choice.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — A deep link is "inert until Enter": the prompt is pre-filled but nothing reaches the model and normal permission rules / `CLAUDE.md` / trust prompts apply — the consent-gating posture this term covers.
- [Skills](../../term_dictionary/term_skills.md) — The deep-links page recommends storing a long runbook prompt as a `/skill` so the link's `q` parameter only names it — the packaged-workflow mechanism this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The "choose the right approach" matrix (Dispatch/Remote Control/Channels/Slack/Scheduled) is about triggering agent work while away — the autonomous away-from-terminal modes this term defines.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Deep links seed investigations from runbooks/alerts/dashboards at a known starting point in the right repo — a reproducible launch checkpoint, the durable-starting-point idea this term covers.

## Section Coverage Map

```
claude-code-on-the-web.md
├── GitHub authentication options ──────── → note 8 (auth + access-scope caveat)
├── The cloud environment ─────────────── → note 3
│   ├── What's available in cloud sessions → note 3 (carries-over table)
│   ├── Installed tools ─────────────────── → note 3
│   ├── Work with GitHub issues and PRs ─── → note 3
│   ├── Link artifacts back to the session  → note 3 (CLAUDE_CODE_REMOTE_SESSION_ID)
│   ├── Run tests, start services, packages → note 3
│   ├── Resource limits ─────────────────── → note 3 (Remote Control link-out → note 9)
│   └── Configure your environment ──────── → note 3 (env vars, /remote-env)
├── Setup scripts ─────────────────────── → note 4
│   ├── Environment caching ─────────────── → note 4
│   ├── Setup scripts vs SessionStart hooks → note 4 (→ B07A/B07B hooks)
│   └── Install deps with SessionStart hook → note 4 (→ B07A hooks#sessionstart)
├── Network access ────────────────────── → note 5
│   ├── Access levels ───────────────────── → note 5
│   ├── Allow specific domains ──────────── → note 5
│   ├── GitHub proxy ────────────────────── → note 5
│   ├── Security proxy ──────────────────── → note 5
│   └── Default allowed domains (accordion) → note 5 (summarized by category; not inlined verbatim)
├── Move tasks between web and terminal ── → note 6
│   ├── From terminal to web (+ tips) ───── → note 6 (→ B05A plan mode, B13B ultraplan)
│   ├── Send local repos without GitHub ─── → note 6 (CCR_FORCE_BUNDLE)
│   ├── From web to terminal (teleport) ─── → note 6
│   ├── Teleport requirements ───────────── → note 6
│   └── --teleport is unavailable ───────── → note 6
├── Work with sessions ────────────────── → note 7
│   ├── Manage context ──────────────────── → note 7 (→ B02A compaction, B10A subagents)
│   ├── Review changes ──────────────────── → note 7
│   ├── Share sessions (Ent/Team, Max/Pro)  → note 7
│   ├── Archive / Delete sessions ───────── → note 7
├── Auto-fix pull requests ────────────── → note 7
│   └── How Claude responds to PR activity  → note 7
├── Security and isolation ────────────── → note 8 (→ B16 security)
├── Troubleshooting (cloud) ───────────── → note 8
│   ├── Session creation failed ─────────── → note 8
│   ├── Remote Control session expired ──── → note 8 (→ note 9)
│   └── Environment expired ─────────────── → note 8
├── Limitations ───────────────────────── → note 8 (→ B13B GHES/code-review, B16 ZDR)
└── Related resources ─────────────────── → notes 1/7/9 (links; → B11 routines, B13B ultraplan)
web-quickstart.md
├── (intro) / How sessions run ────────── → note 1
├── Compare ways to run Claude Code ────── → note 1 → note 10 (surface matrix)
├── Connect GitHub and create env ──────── → note 2
│   └── Connect from your terminal ──────── → note 2 (/web-setup)
├── Start a task ──────────────────────── → note 2 (→ B05A permission modes)
├── Pre-fill sessions ─────────────────── → note 2 (claude.ai/code query params)
├── Review and iterate ────────────────── → note 2
├── Troubleshoot setup (8 H3) ─────────── → note 8 (cloud troubleshooting)
└── Next steps ────────────────────────── → notes 1/2 (links; → B11 routines, B02B memory)
remote-control.md
├── (intro) / Requirements ────────────── → note 9
├── Start a Remote Control session ─────── → note 9
│   ├── Connect from another device ─────── → note 9
│   └── Enable Remote Control for all ───── → note 9
├── Connection and security ───────────── → note 9
├── Remote Control vs Claude Code on web ─ → note 10
├── Mobile push notifications ──────────── → note 9
├── Limitations ───────────────────────── → note 9 (→ B13B ultraplan)
├── Troubleshooting (6 named errors) ───── → note 9 (→ B14A providers, B14B managed settings)
├── Choose the right approach (matrix) ─── → note 10 (→ B12A Dispatch, B08B Channels, B13A Slack, B11 scheduled)
└── Related resources ─────────────────── → notes 9/10 (links)
deep-links.md
├── (intro) / How it works ────────────── → note 10
│   └── What a launched session shows ───── → note 10 (inert-until-Enter, external-link warning)
├── Build a link ──────────────────────── → note 10 (q/cwd/repo params)
│   └── Choose between cwd and repo ─────── → note 10
├── Examples ──────────────────────────── → note 10
│   ├── Embed a link in a runbook ───────── → note 10
│   └── Open a link from the shell ──────── → note 10 (macOS/Linux/Windows)
├── Registration and supported platforms ─ → note 10 (→ B03A settings disableDeepLinkRegistration)
├── Open a VS Code tab instead of terminal  → note 10 (→ B12A vs-code)
├── Troubleshooting (4 named issues) ───── → note 10
└── Learn more ────────────────────────── → note 10 (links; → B06 skills, B11 headless)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| claude-code-on-the-web (6.3Kw, 11 H2, 26 H3 — far >2500w) | notes 3,4,5,6,7,8 + GitHub-auth/security/limits folded to note 8 | Exceeds density cap ~2.5×; cleanly separable by BB and topic — cloud-environment model (concept, note 3) vs setup-scripts (procedure, note 4) vs network model (concept, note 5) vs move-tasks (procedure, note 6) vs session-management+auto-fix (procedure, note 7) vs security/auth/limits/troubleshooting (concept, note 8). Sessions/context/hooks/MCP/subagents linked out, not duplicated. |
| web-quickstart (2.5Kw) | notes 1 (intro/how-sessions-run/compare), 2 (connect/start/review procedure); troubleshoot-setup → note 8 | Mixed BB: the "what/why/compare" framing is concept (note 1, paired with on-the-web intro), the connect→submit→review walkthrough is procedure (note 2), and the setup-troubleshooting belongs with note 8's cloud troubleshooting to avoid a thin standalone note. |
| remote-control (3.0Kw) | note 9 (setup procedure), note 10 (vs-web + choose-approach concept, paired with deep-links) | Mixed BB: start/connect/push-notifications is procedure (note 9); the comparison/decision matrices are concept and naturally pair with deep-links' decision-aid material (note 10), keeping note 9 under the cap. |
| deep-links (1.9Kw) | folded into note 10 | Under cap as a single note; its concept (how-it-works/safety) + build/embed procedure are tightly coupled and pair with the remote-vs-web decision aids into one cross-surface "launch/choose" note. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_web_overview | concept | 450 | 0 | ✅ |
| 2 | cc_web_quickstart | procedure | 600 | 1 | ✅ |
| 3 | cc_cloud_environment | concept | 650 | 2 | ✅ |
| 4 | cc_web_setup_scripts | procedure | 550 | 2 | ✅ |
| 5 | cc_cloud_network_access | concept | 550 | 1 | ✅ |
| 6 | cc_move_tasks_web_terminal | procedure | 600 | 2 | ✅ |
| 7 | cc_web_session_management | procedure | 600 | 0 | ✅ |
| 8 | cc_web_security_and_limits | concept | 550 | 0 | ✅ |
| 9 | cc_remote_control | procedure | 750 | 2 | ✅ |
| 10 | cc_remote_vs_web_and_deep_links | concept | 600 | 2 | ✅ |

No note approaches the caps (max ~750w vs 2,500w cap; max 2 code blocks vs 6 cap). The source's large default-domain accordion is summarized by category in note 5 (not inlined verbatim — it is a reference allowlist, not load-bearing prose). No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_web_overview cc_web_quickstart cc_cloud_environment cc_web_setup_scripts cc_cloud_network_access cc_move_tasks_web_terminal cc_web_session_management cc_web_security_and_limits cc_remote_control cc_remote_vs_web_and_deep_links"
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

Single phase (10 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability (inbound) | each of the 10 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (entry-point) | each note is reachable from `entry_claude_code_docs.md` (rows contributed at execution) | DB query + entry-point row check |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 10 rows** under a
"Web & Remote Surfaces" cluster + increments the BB-distribution counts (concept +5, procedure +5).

## Undigested Terms Plan (Step 4e)

b12b creates **no new `term_dictionary` notes**. The vocabulary these 4 pages introduce is covered by a b12b
`cc_` doc note, an existing substantive term note (link), or its home sub-plan (Pattern B):

| Term / concept | Disposition |
|---|---|
| Remote Control | note 9 `cc_remote_control` (doc concept — master assigns B12B as owner) |
| Teleport (`--teleport`/`/teleport`) | note 6 `cc_move_tasks_web_terminal` (doc concept — master assigns B12B as owner) |
| Claude Code on the web / cloud session | notes 1,3 (doc concept) |
| Deep link / `claude-cli://` URL scheme | note 10 `cc_remote_vs_web_and_deep_links` (doc concept) |
| Setup script / environment caching | note 4 (doc concept) |
| Network access level / GitHub proxy / security proxy | note 5 (doc concept); proxy mechanics → link `term_reverse_proxy`, `term_proxy_pattern` (exist) |
| Auto-fix pull requests | note 7 (doc concept) |
| Cloud environment / environment variables | note 3 (doc concept) |
| Dispatch | linked out to B12A (`desktop#sessions-from-dispatch`) — owned there per master |
| Sandbox / Sandboxing | existing term notes (link `term_sandbox`, `term_sandbox_backend`) |
| Subagent / Agent teams / MCP / Context window / Compaction / Skills | existing term notes (link) |
| Permission mode / Plan mode | link `term_graduated_trust` (exists); full ref owned by B05A |
| SessionStart hook | owned by B07A/B07B (`hooks#sessionstart`) — linked out, captured there |
| Worktree | owned by B10B (`worktrees`) — linked out, captured there |
| OAuth / `/login` / login token / `gh` token | link `term_oauth_token` (exists); auth page owned by B14B |
| Routines / Scheduled tasks / Channels / Slack / Ultraplan | owned by B11/B08B/B13A/B13B — linked out, captured there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/MDX
callouts for newly-surfaced terms. No new cross-cutting vocabulary term with no doc-page home AND no
existing note surfaced — every concept is either digested as a b12b `cc_` doc note or linked to an existing
term / its home sub-plan. **0 new B12B `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B12B authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these page concepts duplicate existing notes?) was
performed: `term_sandbox`, `term_sandbox_backend`, `term_mcp`, `term_subagent`, `term_context_window`,
`term_compaction`, `term_skills`, `term_graduated_trust`, `term_reverse_proxy`, `term_proxy_pattern`,
`term_oauth_token`, `term_tls_pinning`, `term_claude_code`, `term_agent_harness`,
`term_autonomous_coding_agents`, `term_multi_agent`, `term_agentic_memory`, `term_context_engineering`,
`term_regular_checkpointing` all exist → linked, not recreated. Dedup against `documentation/` confirmed: no

## Term-Note Authoring Requirements

**N/A for b12b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (Bash/JSON/URL snippets copied exactly from source). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 in-degree ≥1 each):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 9, 10 | product term → web/remote-control surfaces + cross-surface comparison |
| `term_dictionary/term_sandbox.md` | notes 3, 8 | sandbox term → cloud-environment VM + isolation/security |
| `term_dictionary/term_reverse_proxy.md` | note 5 | reverse-proxy term → GitHub/security proxy network model |
| `term_dictionary/term_oauth_token.md` | notes 2, 9 | token term → GitHub/`/web-setup` connect + Remote Control auth |
| `term_dictionary/term_autonomous_coding_agents.md` | notes 1, 6 | autonomous-agent term → web "tasks that don't need steering" + move-tasks |
| `term_dictionary/term_compaction.md` | note 7 | compaction term → cloud-session context management |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | notes 1, 2 | getting-started tutorial → web overview + quickstart |

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 10 rows for `entry_claude_code_docs.md` under a "Web & Remote Surfaces" cluster; `/tessellum-check-broken-links`.
- Verify the forward link-outs to sibling sub-plans (B02A/B02B/B05A/B05B/B07A/B07B/B08A/B10A/B10B/B11/B12A/B13A/B13B/B14B/B16/B17) resolve once those sub-plans execute; until then keep them as prose-qualified links per master cross-reference policy.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13** — see Review Sign-Off below (9/9 → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B12B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/`; measured words match the master's figures (on-the-web 6,326 · web-quickstart 2,497 · remote-control 2,973 · deep-links 1,875 = 13,671). The 6.3Kw on-the-web page is ~2.5× the density cap → split into 6 notes (documented in Split Decisions); no >1.5× under-estimate elsewhere.
- **Notes**: 10 (concept 5, procedure 5) — matches master estimate exactly. Splits documented for all 4 pages.
- **Step 2d new-term scan**: 0 new cross-cutting terms surfaced → **0 new B12B term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5/G7/G8 verification notes, full Section Coverage Map with link-outs.
- **28-item checklist**: PASS (term-note items N/A — B12B authors no terms; entry-point + undigested-terms inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7 inbound-discoverability + G8 entry-point reachability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B12B contributes 10 rows under a "Web & Remote Surfaces" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 10 notes 450–750w, ≤2 code blocks — none borderline; the 6.3Kw page was split into 6 notes, not compressed. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` spot-check: on-the-web measured 6,326 = plan 6,326; remote-control 2,973 = plan 2,973; deep-links 1,875 = plan 1,875; web-quickstart 2,497 = plan 2,497. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B12B authors 0 term notes; Undigested Terms Plan routes every page term to a `cc_` note / existing term / home sub-plan; Authoring Requirements inherited. Step 2d found 0 new terms. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
