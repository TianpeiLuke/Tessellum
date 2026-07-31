---
title: Sub-Plan B05B — Claude Code Docs: Sandboxing
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["sandbox-environments", "sandboxing"]
---

# Sub-Plan B05B: Sandboxing

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 2 sandboxing/isolation pages: how to choose an isolation environment (per-command Bash sandbox →
sandbox runtime → dev/custom container → VM → Claude Code on the web) and how to configure the built-in
sandboxed Bash tool (enable, modes, filesystem/network/OS isolation, permission interaction, org
enforcement, troubleshooting, limitations). P2 (Phase B) — builds on the permission cores (B05A) and the
agentic-loop/tools foundations (B01A), so it runs after them. The existing `term_sandbox` term note is
LINKED (not recreated); these are `cc_` *documentation* notes about Claude Code's concrete sandbox
features, dedup-distinct from the general `term_sandbox` concept.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 6,056 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the concrete Claude Code sandbox mechanics that other sub-plans link — the comparison of
  isolation approaches (B05B is the home for the sandbox-environments decision matrix), the `/sandbox`
  enable flow, and how the Bash sandbox relates to permission rules/modes (the B05A bridge).
- **Group**: split the large `sandboxing.md` (4.1Kw, 8 H2 / 13 H3) by BB — setup procedure vs modes concept
  vs isolation-mechanism concept vs permission-relationship concept vs org-enforcement procedure vs
  limitations concept. Keep `sandbox-environments.md` (1.9Kw) as the comparison/choose concept note, with
  the runtime+containers+VM+web setups as a sibling procedure note.
- **Skip / link-out (own other sub-plans)**: permission rules → B05A `permissions.md`; permission modes /
  auto mode / `--dangerously-skip-permissions` / protected paths → B05A `permission-modes.md` /
  `auto-mode-config.md`; dev container detail → B15A `devcontainer.md`; Claude Code on the web detail →
  B12B `claude-code-on-the-web.md`; settings keys reference → B03A `settings.md`; security model → B16
  `security.md`; Agent SDK secure deployment → B21A `secure-deployment.md`; computer use → B13A; env-var
  `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` → B03A `env-vars.md`; data usage → B16 `data-usage.md`. Referenced via
  links, never duplicated.
- **Terms**: the `Sandboxing` glossary term maps to the existing `term_sandbox` note (link, Pattern B) — no
  new `term_dictionary` capture (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| sandbox-environments | /sandbox-environments | 1,944 | 1 | 10 | 1 | concept (compare/choose) |
| sandboxing | /sandboxing | 4,112 | 7 | 8 | 13 | concept/procedure |

> Code-block counts are fenced-pair counts (`grep -c '^\`\`\`'` ÷ 2 = 1 and 7 respectively;
> sandbox-environments has 1 bash fence, sandboxing has 7 fences across the setup/config examples).

> **H2 lists (document order):**
> - **sandbox-environments**: Compare sandboxing approaches · Choose an approach (H3 How isolation relates
>   to permission modes) · Sandboxed Bash tool · Sandbox runtime · Dev containers · Custom container ·
>   Virtual machine · Claude Code on the web · Enforce isolation across an organization · See also
> - **sandboxing**: Get started (H3 Set up Linux and WSL2, Sandbox modes) · Configure sandboxing · How
>   sandboxing works (H3 Filesystem isolation, Network isolation, OS-level enforcement) · How sandboxing
>   relates to permissions and permission modes (H3 Permission rules, Permission modes) · Configure the
>   sandbox for your organization (H3 Enforce sandboxing with managed settings, Keep developers from
>   widening the policy, Custom proxy configuration) · Troubleshooting · Limitations (H3 Security
>   limitations, Platform and tool compatibility, Scope) · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (master estimate
was 6; +2 because `sandboxing.md` is 4.1Kw / 8 H2 / 13 H3 and splits BB-cleanly — see Split Decisions).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sandbox_environments_comparison.md` | concept | sandbox-environments: Compare approaches, Choose an approach, the 6 environment sections (Bash tool/runtime/dev container/custom container/VM/web at a glance), How isolation relates to permission modes | 600 | The isolation decision matrix: what each approach isolates, Docker requirement, setup effort; goal→approach table; how isolation layers with permission modes (`--dangerously-skip-permissions` needs a boundary, auto mode adds defense-in-depth). Detail/setup → note 2; per-command Bash tool → notes 3–8; dev container → B15A; web → B12B. |
| 2 | `cc_sandbox_runtime_and_containers.md` | procedure | sandbox-environments: Sandbox runtime, Dev containers, Custom container, Virtual machine, Claude Code on the web | 500 | Whole-process isolation setups: `@anthropic-ai/sandbox-runtime` (deny-by-default, `~/.srt-settings.json`, `npx … claude`), dev container (default-deny iptables), custom OCI container, dedicated VM/microVM, Anthropic-hosted web VM. Links B15A devcontainer, B12B web. |
| 3 | `cc_sandboxed_bash_tool_setup.md` | procedure | sandboxing: Get started (Run /sandbox, Choose a mode, Run a Bash command), Set up Linux and WSL2 | 500 | Enable the Bash sandbox: `/sandbox` panel (Mode/Overrides/Config tabs), settings scopes (`.claude/settings.local.json`, `sandbox.enabled`, `failIfUnavailable`), Linux/WSL2 deps (`bubblewrap`, `socat`, seccomp), Ubuntu 24.04 AppArmor + WSL2 notes. |
| 4 | `cc_sandbox_modes.md` | concept | sandboxing: Sandbox modes (auto-allow vs regular, deny/ask exceptions, escape hatch, strict mode, `$TMPDIR`) | 450 | Auto-allow vs regular-permissions modes; what still prompts in auto-allow (deny rules, `rm /`, content-scoped ask rules); the `dangerouslyDisableSandbox` escape hatch + `allowUnsandboxedCommands`/strict mode; session-temp `$TMPDIR`. |
| 5 | `cc_sandbox_filesystem_network_isolation.md` | concept | sandboxing: Configure sandboxing (allowWrite/denyRead path prefixes), How sandboxing works (Filesystem isolation, Network isolation, OS-level enforcement) | 600 | How the boundary works: default write (cwd + temp) / default read (whole computer minus denies), `sandbox.filesystem.allow/deny` + path prefixes, git-worktree `.git` exception, proxy-based domain allowlist (`allowedDomains`/`allowManagedDomainsOnly`), Seatbelt/bubblewrap OS enforcement, child-process inheritance. |
| 6 | `cc_sandbox_vs_permissions.md` | concept | sandboxing: How sandboxing relates to permissions and permission modes (Permission rules, Permission modes) | 450 | The complementary-layers model: permission rules (pre-run, all tools) vs sandbox (OS-enforced, Bash + children); the fs/network setting-vs-rule mapping table; `/sandbox` is NOT a permission mode; auto-allow ≠ auto mode. Bridges B05A. |
| 7 | `cc_sandbox_org_enforcement.md` | procedure | sandboxing: Configure the sandbox for your organization (Enforce with managed settings, Keep developers from widening the policy, Custom proxy configuration); sandbox-environments: Enforce isolation across an organization | 450 | Admin enforcement: managed-settings JSON (`enabled`/`failIfUnavailable`/`allowUnsandboxedCommands:false`), MDM vs server-managed delivery, boolean-override vs array-merge semantics, `allowManagedReadPathsOnly`/`allowManagedDomainsOnly` lockdown, custom MITM proxy ports; which approaches an org can actually enforce. Links B03A settings, B14B server-managed. |
| 8 | `cc_sandbox_limitations_and_troubleshooting.md` | concept | sandboxing: Troubleshooting, Limitations (Security limitations, Platform and tool compatibility, Scope) | 600 | Security limits (no-TLS-inspection / domain fronting, Unix-socket & filesystem escalation, weaker-nested-sandbox caveat, settings-file protection); platform support (macOS/Linux/WSL2 only); scope (file tools, computer use, env vars, subagents); common command fixes (`jest --no-watchman`, Go-CLI TLS, `docker` excluded, `--dangerously-skip-permissions` as root). |

**Estimate: 8 notes** — concept ×5 (notes 1, 4, 5, 6, 8), procedure ×3 (notes 2, 3, 7). All single-BB, all
within caps. (Master estimate 6; +2 is BB-driven: `sandboxing.md`'s 8 H2 / 13 H3 cover six distinct topics
that split one-per-BB — setup / modes / isolation / permissions / org / limitations.)

## Summary Statistics & Building Block Distribution

- Source pages: 2 (6,056 words). New `cc_` notes: **8**. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,150 (avg ~520/note). Code blocks: source has 8 fenced examples; reproduced
  selectively in the procedure/isolation notes (3, 5, 7) — each note well under the ≤6 cap.
- **Building Block Distribution**: concept ×5 (notes 1, 4, 5, 6, 8) · procedure ×3 (notes 2, 3, 7). No
  model/argument/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (13 distinct `term_dictionary/` terms across the

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> `- [Term](../../term_dictionary/term_*.md) — <what-it-is>; relevance: <why it matters to THIS note>`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are

### 1. `cc_sandbox_environments_comparison` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment with a security boundary; relevance: this note is the canonical comparison of Claude Code's sandbox/isolation environments, so the general sandbox concept is its definitional anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: every isolation approach here wraps the Claude Code process or its Bash commands, so the product term grounds what is being isolated.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission modes that widen autonomy as trust grows; relevance: the note's "How isolation relates to permission modes" section pairs each isolation boundary with a permission mode (`--dangerously-skip-permissions`, auto mode, default) to decide how much autonomy is safe.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that plan/edit/run/verify code unattended; relevance: the comparison exists precisely to make unattended autonomous runs (work-when-away, untrusted repos) safe by choosing the right isolation strength.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny / fail-safe-defaults permission pattern; relevance: the stronger approaches (dev container default-deny firewall, sandbox runtime denying all write/network by default) embody the deny-first posture the note recommends for unattended work.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls bounding agent behavior; relevance: an isolation boundary is the OS-level guardrail the note layers under permission controls so an agent's actions are contained even when prompts are removed.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the wrapper that gives an LLM tools, context, and an execution environment; relevance: the "whole Claude Code process" approaches put the entire harness (file tools, MCP servers, hooks) inside the boundary, the distinction the comparison table turns on.

### 2. `cc_sandbox_runtime_and_containers` (6 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment with a security boundary; relevance: this note documents the whole-process sandbox setups (runtime, containers, VMs) that realize the sandbox concept beyond the per-command Bash tool.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: each setup here (`npx @anthropic-ai/sandbox-runtime claude`, dev container, custom OCI image, VM, hosted web) wraps the Claude Code process being isolated.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the wrapper providing tools, context, and execution environment; relevance: the runtime constrains every tool, hook, and MCP server in the session, i.e. it isolates the entire harness, not just Bash.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — protocol for connecting external tools/data to the agent; relevance: the note's selling point for runtime/containers is that MCP servers (separate host processes) come inside the boundary, which the per-command Bash sandbox cannot do.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents that operate unattended; relevance: these container/VM setups are the recommended boundaries for `--dangerously-skip-permissions` and untrusted-repo work, the autonomous operating modes the note targets.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: the sandbox runtime denies all write and network access by default and the example dev container ships a default-deny iptables firewall — both concrete deny-first configurations the note explains.

### 3. `cc_sandboxed_bash_tool_setup` (6 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: this note is the enable/setup procedure for Claude Code's built-in Bash sandbox, the core subject the sandbox concept describes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: the `/sandbox` command, settings scopes, and dependency checks documented here are Claude Code features the note walks through configuring.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission/trust controls; relevance: the Mode tab choice (auto-allow vs regular permissions) the setup walks through is exactly the trust dial that decides whether sandboxed commands prompt.
- [Deny-First](../../term_dictionary/term_deny_first.md) — fail-safe-defaults pattern; relevance: `sandbox.failIfUnavailable: true` makes a missing dependency a hard failure rather than silently running unsandboxed — the fail-safe default the setup note recommends for managed gates.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS-level filesystem permission primitives; relevance: the Linux/WSL2 setup installs `bubblewrap` and configures AppArmor user namespaces, the OS permission machinery the sandbox builds on.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents running with fewer prompts; relevance: enabling the sandbox is the prerequisite for letting Claude run most shell commands without per-command approval, the autonomy this setup unlocks.

### 4. `cc_sandbox_modes` (6 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: this note details the two approval modes of that sandbox (auto-allow vs regular) and how the boundary itself replaces the per-command prompt.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission modes; relevance: auto-allow mode auto-approves sandboxed commands because the boundary contains them, a distinct trust level from the regular-permissions mode the note contrasts.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: even in auto-allow, explicit deny rules and `rm /` guards always win, and strict mode (`allowUnsandboxedCommands:false`) refuses any unsandboxed fallback — the deny-first exceptions the note enumerates.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: the modes, the `dangerouslyDisableSandbox` escape hatch, and `$TMPDIR` handling are all Claude Code Bash-sandbox behaviors this note specifies.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls; relevance: the always-on guards (deny rules, critical-path `rm` prompts, content-scoped ask rules) are the guardrails that hold even when auto-allow removes routine prompts.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agents running with fewer prompts; relevance: auto-allow mode is the mechanism that lets the agent execute file-modifying Bash without prompting, working independently of the accept-edits permission mode.

### 5. `cc_sandbox_filesystem_network_isolation` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment with a security boundary; relevance: this note explains the actual filesystem/network/OS mechanics that make the sandbox a boundary, the implementation behind the concept.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS filesystem permission primitives; relevance: default write (cwd + temp), default read (whole computer minus denies), and `allowWrite`/`denyRead` path rules are OS-enforced filesystem permissions the note configures.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: `sandbox.filesystem.*` settings, path prefixes, the git-worktree `.git` exception, and `allowedDomains` are Claude Code sandbox config the note documents.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: network access starts with no pre-allowed domains (prompt-on-first-use, or block under `allowManagedDomainsOnly`), a deny-first network posture the note describes.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls; relevance: the OS-level enforcement (Seatbelt/bubblewrap) is the guardrail that holds on the running process regardless of what the model chose to run, even for child processes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission controls; relevance: widening the boundary via `allowWrite`/`allowedDomains` is the controlled trust expansion the note frames as a deliberate, scoped decision.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the wrapper providing the execution environment; relevance: these same OS primitives are exposed as the standalone sandbox-runtime package that wraps the whole harness, which the note cross-references.

### 6. `cc_sandbox_vs_permissions` (7 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission modes; relevance: this note's central table contrasts `/sandbox` with auto mode and `--dangerously-skip-permissions` — the permission modes the graduated-trust ladder defines — clarifying that the sandbox is not itself a permission mode.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the note positions the sandbox as the OS-enforced layer complementary to (not a replacement for) permission rules and modes.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: the note's setting-vs-rule mapping shows how deny rules and sandbox deny paths combine, with the most restrictive (deny) winning — the deny-first evaluation order.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS filesystem permission primitives; relevance: the note distinguishes permission rules (pre-run, command-string based) from sandbox filesystem/network limits (OS-enforced on the process), the dual-layer model it explains.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: the permission-rule / sandbox-setting interaction (merged into the final sandbox config) is a Claude Code policy-resolution behavior the note specifies.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls; relevance: the note frames sandbox + permission rules + permission modes as complementary guardrail layers, with the OS boundary holding even when a permission decision is wrong.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human review/approval in an automated process; relevance: the note explains what still forces a human prompt (ask rules, regular-permissions mode) versus what the sandbox auto-approves, the HITL trade-off it documents.

### 7. `cc_sandbox_org_enforcement` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: this note is how an organization requires the Bash sandbox for every developer and prevents them from widening the policy.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — progressive permission/trust controls; relevance: managed settings cap how far developers can widen trust (boolean overrides ignored, `allowManagedReadPathsOnly`), the centrally-controlled trust ceiling the note configures.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: the recommended managed config (`failIfUnavailable:true`, `allowUnsandboxedCommands:false`) makes the sandbox a fail-closed security gate — a deny-first organizational default.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: managed settings, MDM/server-managed delivery, and array-merge-vs-boolean-override semantics are Claude Code policy mechanisms the note deploys.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS filesystem permission primitives; relevance: the note's managed `denyRead` for credential dirs (`~/.aws`, `~/.ssh`) and `allowManagedReadPathsOnly` lockdown are filesystem permission controls administered centrally.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls; relevance: org enforcement turns the sandbox into a mandated guardrail (cannot be disabled locally), plus a custom MITM proxy for inspecting/logging egress — defense layers the note adds.
- [Values-Over-Rules](../../term_dictionary/term_values_over_rules.md) — governance via principles rather than exhaustive rules; relevance: the note warns `excludedCommands` has no managed-only lockdown so admins must "keep the managed list narrow" — a judgment/values call where rules alone cannot enforce intent.

### 8. `cc_sandbox_limitations_and_troubleshooting` (7 term notes)
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: this note states where the Claude Code sandbox stops being a hard boundary (TLS-blind proxy, Unix-socket/filesystem escalation, weaker-nested mode) and how to fix common command failures.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety controls and their gaps; relevance: the note is the explicit limitations register — where the sandbox guardrail can be bypassed (domain fronting, `docker.sock`) and must be backstopped by other controls.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — techniques that exploit a system's blind spots; relevance: domain fronting past the hostname-only allowlist and privilege escalation via allowed Unix sockets are the adversarial bypasses the security-limitations section warns against.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny permission pattern; relevance: the note's mitigation (narrow `allowedDomains`, `denyRead` credential dirs, avoid broad `allowWrite`) reasserts deny-first because broad allows undo the boundary on the other side.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — OS filesystem permission primitives; relevance: filesystem-permission escalation (writes to `$PATH` dirs, `.bashrc`, system config) leading to code execution in other security contexts is a core limitation the note details.
- [Subagent](../../term_dictionary/term_subagent.md) — an isolated worker spawned by the main agent; relevance: the Scope section clarifies subagents run in the same process and inherit the parent's sandbox config — so Bash inside a subagent is sandboxed too, a scope nuance the note states.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: the troubleshooting fixes (`jest --no-watchman`, `excludedCommands` for Go CLIs / `docker`, `--dangerously-skip-permissions` blocked as root) and scope items (file tools, computer use, env scrub, subagents) are Claude Code sandbox behaviors the note resolves.

## Section Coverage Map

```
sandbox-environments.md
├── Compare sandboxing approaches (table) ──────────── → note 1 (cc_sandbox_environments_comparison)
├── Choose an approach (goal→approach table) ───────── → note 1
│   └── How isolation relates to permission modes ──── → note 1 (→ B05A permission-modes / auto-mode-config)
├── Sandboxed Bash tool (intro) ───────────────────── → note 1 (at-a-glance) → notes 3–8 (detail)
├── Sandbox runtime ───────────────────────────────── → note 2 (cc_sandbox_runtime_and_containers)
├── Dev containers ────────────────────────────────── → note 2 (→ B15A devcontainer.md detail)
├── Custom container ──────────────────────────────── → note 2
├── Virtual machine ───────────────────────────────── → note 2
├── Claude Code on the web ────────────────────────── → note 2 (→ B12B claude-code-on-the-web.md detail)
├── Enforce isolation across an organization ──────── → note 7 (cc_sandbox_org_enforcement)
└── See also (links) ──────────────────────────────── → notes 1/7 (links: security B16, secure-deployment B21A, settings B03A)
sandboxing.md
├── Get started (Run /sandbox, Choose mode, Run cmd) ─ → note 3 (cc_sandboxed_bash_tool_setup)
│   ├── Set up Linux and WSL2 ──────────────────────── → note 3
│   └── Sandbox modes ──────────────────────────────── → note 4 (cc_sandbox_modes)
├── Configure sandboxing (allowWrite/denyRead paths) ─ → note 5 (cc_sandbox_filesystem_network_isolation)
├── How sandboxing works ──────────────────────────── → note 5
│   ├── Filesystem isolation ───────────────────────── → note 5
│   ├── Network isolation ──────────────────────────── → note 5
│   └── OS-level enforcement ───────────────────────── → note 5
├── How sandboxing relates to permissions & modes ─── → note 6 (cc_sandbox_vs_permissions)
│   ├── Permission rules ───────────────────────────── → note 6 (→ B05A permissions.md)
│   └── Permission modes ───────────────────────────── → note 6 (→ B05A permission-modes.md)
├── Configure the sandbox for your organization ───── → note 7
│   ├── Enforce sandboxing with managed settings ───── → note 7 (→ B03A settings, B14B server-managed)
│   ├── Keep developers from widening the policy ───── → note 7
│   └── Custom proxy configuration ─────────────────── → note 7
├── Troubleshooting ───────────────────────────────── → note 8 (cc_sandbox_limitations_and_troubleshooting)
├── Limitations ───────────────────────────────────── → note 8
│   ├── Security limitations ───────────────────────── → note 8 (→ B16 security.md)
│   ├── Platform and tool compatibility ────────────── → note 8
│   └── Scope (file tools, computer use, env, subagents) → note 8 (→ B13A computer-use, B03A env-vars, B10A sub-agents)
└── See also (links) ──────────────────────────────── → notes 1/5/6 (links)
```
No orphaned sections. Sections owned by other sub-plans (permission rules/modes B05A, devcontainer B15A,
web B12B, settings/env B03A, security B16, computer use B13A) are LINKED, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| sandboxing.md (4.1Kw, 8 H2 / 13 H3, mixed BB) | notes 3, 4, 5, 6, 7, 8 + link-outs | exceeds the 2,500-word cap and mixes BBs: setup (procedure) / modes (concept) / fs+network isolation (concept) / permission relationship (concept) / org enforcement (procedure) / limitations+troubleshooting (concept). Each splits cleanly to one BB and stays well under caps. |
| sandbox-environments.md (1.9Kw, 10 H2) | notes 1, 2 + link-outs | the compare/choose decision matrix + permission-mode relationship (concept) is distinct from the runtime/container/VM/web setup walkthroughs (procedure); separating keeps each single-BB. |
| Master estimate (6 notes) | locked at **8** | `sandboxing.md`'s 8 H2 / 13 H3 cover six distinct topics; folding any two would either break the one-BB-per-note rule or push a note past comfortable size. +2 over estimate is BB-driven, not padding. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sandbox_environments_comparison | concept | 600 | 0 | ✅ |
| 2 | cc_sandbox_runtime_and_containers | procedure | 500 | 1 | ✅ |
| 3 | cc_sandboxed_bash_tool_setup | procedure | 500 | 3 | ✅ |
| 4 | cc_sandbox_modes | concept | 450 | 0 | ✅ |
| 5 | cc_sandbox_filesystem_network_isolation | concept | 600 | 2 | ✅ |
| 6 | cc_sandbox_vs_permissions | concept | 450 | 0 | ✅ |
| 7 | cc_sandbox_org_enforcement | procedure | 450 | 2 | ✅ |
| 8 | cc_sandbox_limitations_and_troubleshooting | concept | 600 | 0 | ✅ |

No note approaches the caps (≤2,500 words / ≤6 code / ≤400 lines). The 8 source code fences distribute
across notes 2, 3, 5, 7 (the setup/config notes), each ≤3. No over-compression — every H2/H3 maps to a note
or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sandbox_environments_comparison cc_sandbox_runtime_and_containers cc_sandboxed_bash_tool_setup cc_sandbox_modes cc_sandbox_filesystem_network_isolation cc_sandbox_vs_permissions cc_sandbox_org_enforcement cc_sandbox_limitations_and_troubleshooting"
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

Single phase (8 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (in-degree ≥1) | DB confirms in-degree ≥1 for all 8 notes after inlinks applied (anti-island) | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md` (created as a pre-step before the first sub-plan executes);
this sub-plan **contributes its 8 rows** under a "Permissions & Sandboxing" cluster + increments the
BB-distribution counts (concept ×5, procedure ×3). Each note's `## Related Notes` gets the
`entry_claude_code_docs.md` back-link at finalization.

## Undigested Terms Plan (Step 4e)

b05b creates **no new `term_dictionary` notes** — the only vocabulary term these pages introduce as a
glossary-level concept is **Sandboxing**, which is covered by the existing substantive `term_sandbox` note
(link, Pattern B). All other named items are either Claude Code feature names digested into the `cc_` notes
or terms owned by other sub-plans:

| Term / named item | Disposition |
|---|---|
| Sandboxing / sandbox | link `term_sandbox` (exists, substantive) — not recreated |
| Sandboxed Bash tool / sandbox runtime / dev container / custom container / VM / web | Claude Code feature names → digested into b05b `cc_` notes (1–8), not term notes |
| Permission rules / permission modes / auto mode / `--dangerously-skip-permissions` / protected paths | owned by B05A (`permissions`, `permission-modes`, `auto-mode-config`) — linked, captured there |
| Subagent / MCP | existing term notes (link `term_subagent`, `term_mcp`) |
| bubblewrap / Seatbelt / socat / seccomp / Firecracker / iptables / AppArmor / domain fronting | low-level OS/tooling primitives — named inline in the relevant `cc_` note, NOT promoted to term notes (too granular, no vault-wide reuse; Step 10.5f specificity rule) |
| Managed settings / server-managed settings / settings precedence | owned by B03A (`settings`) / B14B (`server-managed-settings`) — linked, captured there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages scanning emphasis/tables/captions/code for
newly-surfaced terms. Candidates considered and rejected for new term-note capture:
- **"domain fronting"** — a security attack technique; relevant but owned by the security cluster (B16
  `security`) if anywhere, and the source links Wikipedia rather than treating it as Claude Code vocabulary;
  named inline in note 8, no new capture.
- **bubblewrap / Seatbelt / socat / seccomp / Firecracker** — OS sandboxing primitives, too granular and
  not vault-reusable (fail the 10.5f specificity bar); named inline in notes 2/3/5/8.
- **"sandbox runtime" (`@anthropic-ai/sandbox-runtime`)** — a Claude Code feature, digested into note 2, not
  a term note (Pattern B: CC features are doc concepts, not `term_dictionary` entries).

**0 new b05b `term_dictionary` captures.** Collision/dedup check across `term_dictionary` AND
`documentation/`: `term_sandbox` exists (linked); no existing `cc_sandbox*` doc note exists in
`resources/documentation/claude_code/` (dir not yet created) → no recreate risk; `term_sandbox_backend` is
an unrelated ML/abuse sandbox (different sense) and is NOT linked.

## Term-Note Authoring Requirements

**N/A for b05b** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (the 8 source fences reproduced exactly in notes 2/3/5/7; do not paraphrase JSON/bash).
- One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 —
2026-06-13.

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_sandbox.md` | notes 1, 3, 5, 8 | sandbox concept → CC sandbox comparison / setup / isolation mechanics / limitations |
| `term_dictionary/term_graduated_trust.md` | notes 4, 6 | permission-mode/trust term → CC sandbox modes + sandbox-vs-permissions |
| `term_dictionary/term_claude_code.md` | notes 1, 2 | product term → CC isolation-environment comparison + whole-process setups |
| `term_dictionary/term_deny_first.md` | note 7 | default-deny pattern → CC org-enforcement managed-settings fail-closed gate |
| `term_dictionary/term_posix_permissions.md` | note 5 | OS filesystem-permission term → CC filesystem/network isolation note |

> Each of the 8 notes receives ≥1 inbound link (notes 1,3,5,8 ← term_sandbox; 4,6 ← term_graduated_trust;
> 2 ← term_claude_code; 7 ← term_deny_first; 5 also ← term_posix_permissions). G7/G8 satisfied by
> construction; verified by DB in-degree query at finalization. The per-sub-plan entry-point back-link from
> `entry_claude_code_docs.md` provides a second inbound edge to all 8.

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8
  rows for `entry_claude_code_docs.md` (Permissions & Sandboxing cluster); `/tessellum-check-broken-links` →
  `/tessellum-fix-broken-links`; verify `note_links` in-degree ≥1 for all 8 (G7/G8) before commit.
- Coordinate cross-links with B05A (permissions) once both land: notes 4/6/7 ↔ B05A permission-mode notes.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B05B, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read fully from `inbox/claude_code_docs/`; measured words match
  the master (sandbox-environments 1,944 · sandboxing 4,112 = 6,056). Measured structure: sandbox-environments
  10 H2 / 1 H3 / 1 code fence; sandboxing 8 H2 / 13 H3 / 7 code fences. The 4.1Kw `sandboxing.md` exceeds the
  2,500-word cap → split confirmed (notes 3–8); no under-estimate.
- **Notes**: locked at **8** (concept 5, procedure 3) — +2 over the master's 6-note estimate, BB-driven (see
  Split Decisions). All single-BB, all within caps.
- **Per-Note Related Notes Mapping (Step 8)**: 6–7 relevancy-selected term notes per note (13 distinct
  `term_openshell`, etc.) discarded; security/agentic-safety terms (`term_deny_first`, `term_guardrails`,
  `term_posix_permissions`, `term_values_over_rules`, `term_human_in_the_loop`, `term_adversarial_attack`)
  kept as genuinely relevant.
- **Step 2d new-term scan**: candidates (domain fronting, bubblewrap/Seatbelt/socat/seccomp/Firecracker,
  sandbox runtime) reviewed → none promoted; **0 new b05b term captures** (Pattern B + 10.5f specificity).
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5 verification note, count-correction lock to 8.
- **28-item checklist**: PASS (term-note items N/A — b05b authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed; set to `ready` after the 9-checkpoint self-review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8 incl G7/G8) | ✅ PASS | 8 gate rows present (single phase), including G7 Discoverability + G8 in-degree ≥1. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B05B contributes 8 rows under Permissions & Sandboxing. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + `## Overview` / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer inherited verbatim from master Format Definition (derived from existing `documentation/` notes). |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–600w, ≤3 code each — none borderline; `sandboxing.md` over-cap already split into 6. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` 2026-06-13: sandbox-environments 1,944 = plan; sandboxing 4,112 = plan; total 6,056 = master. H2/H3/code counts measured via grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | b05b authors 0 term notes; Undigested Terms Plan routes "Sandboxing"→`term_sandbox` (link) + OS primitives inline; Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented — `term_sandbox` exists (linked, not recreated), `term_sandbox_backend` is a different-sense ML/abuse sandbox (not linked), no existing `cc_sandbox*` doc note to duplicate. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
