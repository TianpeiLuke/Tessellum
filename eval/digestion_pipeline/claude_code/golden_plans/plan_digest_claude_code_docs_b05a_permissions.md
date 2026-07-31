---
title: Sub-Plan B05A — Claude Code Docs: Permissions
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["permissions", "permission-modes", "auto-mode-config"]
---

# Sub-Plan B05A: Permissions

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 permissions pages that define Claude Code's fine-grained access-control system: the tiered
permission model and allow/ask/deny rule syntax, the per-tool rule dialects (Bash, PowerShell,
Read/Edit, WebFetch, MCP, Agent, Cd), the six permission modes (default, acceptEdits, plan, auto,
dontAsk, bypassPermissions) and how to switch them, the auto-mode classifier behavior, and the
`autoMode` configuration reference. P1 (Phase A) — permission modes (`term_graduated_trust`) and the
deny-first precedence (`term_deny_first`) are referenced by later batches (sandboxing B05B, hooks
B07, MCP B08, security B16), so this runs early. Glossary terms are routed per Pattern B (see
Undigested Terms Plan), not re-digested.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 9,930 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the allow/ask/deny rule model + deny-first evaluation order, and the six permission
  modes — these are the access-control vocabulary every later sub-plan (sandboxing, hooks, MCP,
  security) links (P1).
- **Group**: split the large `permissions` page (4.8Kw, 12 H2) by topic — system+rule-syntax,
  tool-specific dialects, hooks+working-directories, managed-settings+precedence+sandbox-interaction.
  Split `permission-modes` (3.4Kw) by overview+switching vs per-mode detail, and lift the substantial
  auto-mode section into its own concept note paired with the `auto-mode-config` reference.
- **Skip / link-out (own other sub-plans)**: settings files / settings precedence detail and the full
  permission-settings table → B03A (`settings.md`); sandbox modes / `sandbox.filesystem` /
  `autoAllowBashIfSandboxed` mechanics → B05B (`sandboxing.md`); PreToolUse / PermissionRequest /
  PermissionDenied hook authoring → B07A/B07B (`hooks.md` / `hooks-guide.md`); managed-MCP and
  channel-plugin allowlists → B08A/B08B; server-managed-settings delivery → B14B; CLI flags
  (`--permission-mode`, `--add-dir`, `--dangerously-skip-permissions`) reference → B03B; `/cd`,
  `/add-dir`, `/permissions`, `/plan` command reference → B03B/B06; output styles (Proactive) → B06;
  Ultraplan → B13B; non-interactive `-p` → B11; error reference (auto mode "cannot determine safety")
  → B17. These are referenced via links, never duplicated.
- **Glossary**: not re-digested into `cc_` notes — permission-mode / sandboxing / subagent / MCP terms
  route to existing term notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| permissions | /permissions | 4,793 | 4 | 12 | 16 | concept |
| permission-modes | /permission-modes | 3,377 | 7 | 9 | 6 | concept/procedure |
| auto-mode-config | /auto-mode-config | 1,760 | 6 | 6 | 0 | procedure |

> **H2 lists (document order):**
> - **permissions**: Permission system · Manage permissions · Permission modes · Permission rule syntax (H3 Match all uses of a tool · Use specifiers for fine-grained control · Wildcard patterns · Tool name wildcards) · Tool-specific permission rules (H3 Bash [H4 Compound commands · Process wrappers · Read-only commands] · PowerShell · Read and Edit · WebFetch · MCP · Agent (subagents) · Cd) · Extend permissions with hooks · Working directories (H3 Additional directories grant file access, not configuration) · How permissions interact with sandboxing · Managed settings (H3 Managed-only settings) · Settings precedence · Example configurations · See also
> - **permission-modes**: Available modes · Switch permission modes · Auto-approve file edits with acceptEdits mode · Analyze before you edit with plan mode (H3 Review and approve a plan · Set plan mode as the default) · Eliminate prompts with auto mode (H3 Enable auto mode on Bedrock, Vertex AI, or Foundry · What the classifier blocks by default · Boundaries you state in conversation · When auto mode falls back) · Allow only pre-approved tools with dontAsk mode · Skip all checks with bypassPermissions mode · Protected paths · See also
> - **auto-mode-config**: Where the classifier reads configuration · Define trusted infrastructure · Override the block and allow rules · Inspect the defaults and your effective config · Review denials · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_permission_system_and_rules.md` | concept | permissions: Permission system, Manage permissions, Permission rule syntax (+4 H3) | 650 | Tiered read-only/Bash/file-mod model; allow/ask/deny rules; deny→ask→allow evaluation order (links `term_deny_first`); bare-tool vs scoped deny; rule syntax (match-all, specifiers, `*`/`:*` wildcards, tool-name globs). |
| 2 | `cc_tool_specific_permission_rules.md` | concept | permissions: Tool-specific permission rules (Bash, PowerShell, Read/Edit, WebFetch, MCP, Agent, Cd) | 800 | Per-tool rule dialects: Bash wildcards/word-boundary/compound/process-wrappers/read-only set; PowerShell AST; Read/Edit gitignore anchors + symlink handling; WebFetch `domain:`; MCP `mcp__server__tool`; `Agent(Name)`; `Cd` allowlist. |
| 3 | `cc_permissions_hooks_and_working_directories.md` | concept | permissions: Extend permissions with hooks, Working directories (+1 H3) | 450 | PreToolUse hook permission evaluation (allow/deny/ask, exit-2 block, deny-first preserved → B07); `--add-dir`/`/add-dir`/`additionalDirectories`; config-loading exceptions for `--add-dir` dirs; `/cd` session relocation. |
| 4 | `cc_managed_permission_settings_and_precedence.md` | concept | permissions: Managed settings (+1 H3), Settings precedence, How permissions interact with sandboxing | 600 | Managed (policy) settings that user/project cannot override; managed-only keys (allowManaged*Only, disableBypass/AutoMode, etc.); 5-level settings precedence (deny wins at any level); permissions × sandboxing as complementary defense-in-depth layers. |
| 5 | `cc_permission_modes_overview.md` | concept | permission-modes: intro, Available modes, Switch permission modes | 600 | The six modes (default/acceptEdits/plan/auto/dontAsk/bypassPermissions) and their per-mode tradeoff table (links `term_graduated_trust`); modes set the baseline, rules layer on top; how to switch per interface (Shift+Tab cycle, `--permission-mode`, `defaultMode`, VS Code/Desktop/Web). |
| 6 | `cc_permission_modes_detail.md` | concept | permission-modes: acceptEdits, plan mode (+2 H3), dontAsk, bypassPermissions, Protected paths | 750 | Per-mode behavior: acceptEdits auto-approved filesystem commands + scope; plan mode research-only + plan approval flow; dontAsk allowlist-only; bypassPermissions skip-all + root/sudo refusal + cloud-session ignore; protected-paths table + the protected dirs/files list. |
| 7 | `cc_auto_mode.md` | concept | permission-modes: Eliminate prompts with auto mode (+ classifier blocks/allows, boundaries, fallback, classifier internals) | 700 | Auto mode = classifier-gated autonomous execution; requirements (version/plan/model/provider); enable on Bedrock/Vertex/Foundry; default block vs allow lists; conversational boundaries; fallback thresholds; how the classifier evaluates actions, handles subagents, cost/latency (links `term_guardrails`, `term_values_over_rules`). |
| 8 | `cc_auto_mode_configuration.md` | procedure | auto-mode-config: where config reads, Define trusted infrastructure, Override block/allow rules, Inspect config, Review denials | 600 | `autoMode` settings reference: where the classifier reads config (CLAUDE.md / user / managed scopes); `autoMode.environment` trusted-infra prose entries + `$defaults`; `hard_deny`/`soft_deny`/`allow` 4-tier precedence; `claude auto-mode defaults/config/critique`; reviewing denials + retry. |

**Estimate: 8 notes** — concept ×7 (notes 1–7), procedure ×1 (note 8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (9,930 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,150 (avg ~640/note). Code blocks: ~12 verbatim JSON/bash snippets distributed across notes 1,2,4,5,6,8 (max 5 in any one note — note 8; all ≤6 cap).
- **Building Block Distribution**: concept ×7 (notes 1,2,3,4,5,6,7) · procedure ×1 (note 8). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_permission_system_and_rules` (7 term notes)
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Default-deny security pattern where access is refused unless explicitly allowed; relevance: this note's central rule is the deny→ask→allow evaluation order where a deny match at any level wins and a bare-name deny removes the tool from context — the canonical deny-first/fail-safe-defaults pattern.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Trust spectrum / progressive-autonomy model spanning levels of automation; relevance: the tiered read-only / Bash / file-modification approval model this note defines (and the "Yes, don't ask again" escalation) is exactly graduated trust applied to tool categories.
- [Access Control](../../term_dictionary/term_access_control.md) — Mechanisms that govern which principals may perform which operations on which resources; relevance: allow/ask/deny rules with tool+specifier scoping are an access-control policy language, the subject of this note.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agentic coding tool whose permission system this documents; relevance: the note specifies what the Claude Code agent is allowed to do, so the product term is its definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The runtime that wraps the model with tools and policy; relevance: the note stresses rules are enforced by Claude Code (the harness), not by the model — the harness is precisely where these allow/ask/deny checks live.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The mechanism by which the model invokes tools; relevance: every rule matches a `Tool` or `Tool(specifier)` tool call, so the note's rules gate the model's function-calling/tool-use requests.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — Interactive design where a human approves automated actions; relevance: an `ask` rule and the first-use permission prompt insert a human approval step into the agent loop, the HITL pattern this note's tiered model implements.

### 2. `cc_tool_specific_permission_rules` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool whose per-tool permission dialects this documents; relevance: the note enumerates the rule syntax for each Claude Code built-in tool (Bash, Read, Edit, WebFetch) and extension surface (MCP, Agent), so the product term grounds the whole rule catalog.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The tool-invocation mechanism each rule scopes; relevance: rules like `Bash(npm run *)`, `mcp__puppeteer__navigate`, and `Agent(Explore)` constrain specific tool calls — i.e. they filter the model's function-calling requests per tool.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The protocol exposing external tools as `mcp__server__tool`; relevance: the note has a dedicated MCP rule section (`mcp__puppeteer`, `mcp__server__*` globs) defining how MCP tools are matched and approved.
- [Subagent](../../term_dictionary/term_subagent.md) — A delegated Claude instance invoked as a tool; relevance: the note's `Agent(AgentName)` rules (Explore, Plan, custom) control which subagents Claude may spawn, and `--disallowedTools` disables them.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Default-deny precedence applied across rule types; relevance: the note repeatedly notes deny rules still run before ask/allow regardless of specificity (WebFetch, symlink deny-on-either-path), reinforcing the deny-first ordering for every tool dialect.
- [Access Control](../../term_dictionary/term_access_control.md) — Resource-scoped authorization patterns; relevance: the Read/Edit gitignore anchors (`//`, `~/`, `/`, `./`), WebFetch `domain:` matching, and `Cd` allowlist mode are fine-grained access-control specifiers — the core of this note.

### 3. `cc_permissions_hooks_and_working_directories` (6 term notes)
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Default-deny precedence preserved through hooks; relevance: the note states a PreToolUse hook cannot bypass deny/ask rules and an exit-2 hook blocks before rules are evaluated, so deny-first precedence is preserved even with custom hook logic.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agent whose hook integration and working-dir access this documents; relevance: PreToolUse permission hooks and `--add-dir`/`/cd` are Claude Code runtime features the note describes.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The runtime that fires hooks and bounds the workspace; relevance: PreToolUse hooks run inside the harness's permission pipeline and additional directories extend the harness's file-access scope.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The tool-call event hooks intercept; relevance: PreToolUse hooks run before each tool call's permission prompt and can deny/force-prompt/skip it — they hook the function-calling/tool-use path.
- [Access Control](../../term_dictionary/term_access_control.md) — Scope-bounded resource authorization; relevance: working directories define the file-access boundary (readable without prompts, edit per mode), and the `--add-dir` config-loading exceptions are an access-scope policy this note details.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — Human-approval insertion in automation; relevance: a PreToolUse hook can force a prompt and `/add-dir` of an unfamiliar directory prompts for trust, keeping a human in the approval loop.

### 4. `cc_managed_permission_settings_and_precedence` (7 term notes)
- [Access Control](../../term_dictionary/term_access_control.md) — Centralized policy governing who may configure what; relevance: managed (policy) settings are an organization-level access-control mechanism that user/project settings cannot override — the note's core subject.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Deny-wins precedence across scopes; relevance: the note's precedence rule is that a deny at any level blocks regardless of other allows, and managed deny cannot be loosened by `--allowedTools` — deny-first applied to the settings hierarchy.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Tiered trust / automation-level control; relevance: managed-only keys like `disableBypassPermissionsMode`, `disableAutoMode`, and `allowManagedPermissionRulesOnly` let admins cap how much autonomy users may grant — controlling the trust ceiling.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — OS-level filesystem/network isolation; relevance: the note's "How permissions interact with sandboxing" section pairs permission rules with the sandbox as complementary layers and explains the `autoAllowBashIfSandboxed` interaction.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool whose enterprise configuration this documents; relevance: managed settings, MDM/server-managed delivery, and settings precedence are Claude Code deployment features the note describes.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Runtime safety/policy constraints that cannot be talked around; relevance: managed deny rules and the managed-only locks are hard policy guardrails enforced below the model that an organization deploys for defense-in-depth.
- [CAZ - Contingent Authorization](../../term_dictionary/term_contingent_authorization.md) — Centralized two-person / policy-gated authorization over a population; relevance: like CAZ, managed settings impose an organization-level authorization layer that individual developers cannot self-grant around, the governance model this note formalizes for Claude Code.

### 5. `cc_permission_modes_overview` (6 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Trust spectrum / progressive-autonomy levels; relevance: the six modes (default → acceptEdits → plan → auto → dontAsk → bypassPermissions) ARE a graduated-trust spectrum from full oversight to full autonomy — this note's tradeoff table is the canonical example.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool whose permission modes this documents; relevance: the note defines Claude Code's mode set and the per-interface switching controls (Shift+Tab, `--permission-mode`, `defaultMode`).
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — Degree of human oversight in automation; relevance: default mode reviews each action while looser modes reduce interruptions — modes dial the amount of human-in-the-loop oversight, the note's framing.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Deny/ask rules that apply across all modes; relevance: the note states modes set the baseline but deny and explicit ask rules apply in every mode including bypassPermissions — deny-first persists above the mode setting.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Agents that work in long uninterrupted stretches; relevance: looser modes (auto, bypassPermissions) let Claude work autonomously and report back — the autonomous operating mode this term defines, contrasted with default review.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The runtime that enforces the active mode; relevance: the mode is a harness-level setting (read from settings files / CLI flag) that governs how the harness approves each tool call before it reaches the user.

### 6. `cc_permission_modes_detail` (6 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Progressive-autonomy / trust-level model; relevance: this note details each mode's distinct trust level — acceptEdits (edits + filesystem commands), plan (read-only), dontAsk (allowlist-only), bypassPermissions (skip-all) — the steps of the trust spectrum.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Scoring actions by how reversible/damaging they are; relevance: the protected-paths mechanism and the bypassPermissions circuit breaker for `rm -rf /` / `rm -rf ~` reflect reversibility-weighted risk — the most irreversible actions are never auto-approved even in skip-all mode.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Deny/ask precedence above the mode; relevance: the note notes explicit ask rules force a prompt and deny rules apply even in bypassPermissions, so deny-first overrides the loosest mode.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — Isolated execution environment; relevance: the note recommends bypassPermissions only in isolated containers/VMs/dev containers and notes the root/sudo refusal is skipped inside a recognized sandbox — sandboxing is the safe context for the loosest mode.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — Human-approval gating; relevance: protected-path writes are prompted in default/acceptEdits/plan and the plan-approval flow requires the human to choose how to proceed — modes vary how much human approval each action needs.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool whose per-mode behavior this documents; relevance: acceptEdits scope, plan-mode plan approval, dontAsk CI use, and bypassPermissions flags are Claude Code mode behaviors the note specifies.

### 7. `cc_auto_mode` (8 term notes)
- [Guardrails](../../term_dictionary/term_guardrails.md) — Runtime safety layer that screens actions/content; relevance: auto mode's separate classifier model that blocks escalations, exfiltration, and hostile-content-driven actions — plus the server-side probe scanning tool results — is exactly a runtime guardrail around the agent's actions.
- [Values Over Rules](../../term_dictionary/term_values_over_rules.md) — Principle/intent-based safety vs rigid rule lists; relevance: the auto-mode classifier judges whether an action "escalates beyond your request" and reads conversational boundaries and CLAUDE.md as intent — values/intent-based evaluation layered over the rule-based permission system.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Higher-autonomy trust tier; relevance: auto mode is the high-autonomy point on the mode spectrum — fewer prompts in exchange for classifier-mediated trust, the upper rungs of graduated trust.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Agents that run long tasks without steering; relevance: auto mode lets Claude "execute without routine permission prompts" and keep working without stopping — the autonomous operating mode this term defines.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Deny/ask precedence ahead of the classifier; relevance: the note's classifier decision order resolves allow/deny rules first and explicit ask rules still force a prompt, so deny-first runs before the classifier even in auto mode.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Risk scoring by irreversibility/blast radius; relevance: the classifier blocks "irreversibly destroying files that existed before the session," mass deletion, and production deploys by default — a reversibility-weighted risk policy.
- [Subagent](../../term_dictionary/term_subagent.md) — Delegated isolated-context worker; relevance: the note's "How auto mode handles subagents" accordion describes the classifier checking subagent work at spawn, per-action, and on return — auto-mode safety extended to subagent fan-out.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — Human-fallback on automation failure; relevance: when the classifier blocks 3× consecutively or 20× total, auto mode pauses and resumes prompting — a human-in-the-loop fallback the note documents.

### 8. `cc_auto_mode_configuration` (6 term notes)
- [Guardrails](../../term_dictionary/term_guardrails.md) — Configurable runtime safety policy; relevance: `autoMode.hard_deny`/`soft_deny`/`allow` are the editable rule lists of the auto-mode guardrail classifier, and this note is the reference for tuning them.
- [Values Over Rules](../../term_dictionary/term_values_over_rules.md) — Natural-language, intent-based policy; relevance: every `autoMode` entry is prose read as a natural-language rule ("describe your infrastructure to a new engineer") and explicit user intent overrides soft blocks — values/intent-based configuration, not regex.
- [Access Control](../../term_dictionary/term_access_control.md) — Trusted-resource authorization scoping; relevance: `autoMode.environment` defines which repos/buckets/domains are trusted (everything else is a potential exfiltration target) — an access-scope definition the note configures.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Layered deny precedence; relevance: the note's 4-tier classifier precedence (hard_deny → soft_deny → allow → user intent) and the reminder that `permissions.deny` blocks before the classifier reinforce deny-first across both gates.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — Scoring actions by reversibility; relevance: `soft_deny` is for "destructive actions that user intent can clear" while `hard_deny` is for boundaries that "must never be crossed" — a reversibility/severity-weighted split this note configures.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Org-to-developer trust delegation; relevance: managed `autoMode` entries set organization trust that developers can extend but not remove, tuning how much autonomy the classifier grants — graduated trust applied to infrastructure scope.

## Section Coverage Map

```
permissions.md
├── Permission system (tiered table) ───────── → note 1 (cc_permission_system_and_rules)
├── Manage permissions (allow/ask/deny, order) → note 1
├── Permission modes (defaultMode table) ───── → note 1 intro → note 5 (cc_permission_modes_overview); detail → permission-modes.md owners
├── Permission rule syntax ─────────────────── → note 1
│   ├── Match all uses of a tool ──────────── → note 1
│   ├── Use specifiers for fine-grained ctrl ─ → note 1
│   ├── Wildcard patterns ──────────────────── → note 1
│   └── Tool name wildcards ────────────────── → note 1
├── Tool-specific permission rules ─────────── → note 2 (cc_tool_specific_permission_rules)
│   ├── Bash (+ Compound/Process/Read-only) ── → note 2
│   ├── PowerShell ─────────────────────────── → note 2
│   ├── Read and Edit ──────────────────────── → note 2
│   ├── WebFetch ───────────────────────────── → note 2
│   ├── MCP ────────────────────────────────── → note 2
│   ├── Agent (subagents) ──────────────────── → note 2
│   └── Cd ─────────────────────────────────── → note 2
├── Extend permissions with hooks ──────────── → note 3 (cc_permissions_hooks_and_working_directories) (→ B07 hooks)
├── Working directories ────────────────────── → note 3
│   └── Additional dirs grant file access ──── → note 3
├── How permissions interact with sandboxing ─ → note 4 (cc_managed_permission_settings_and_precedence) (→ B05B sandboxing)
├── Managed settings (+ Managed-only) ──────── → note 4 (→ B14B server-managed-settings)
├── Settings precedence ────────────────────── → note 4 (→ B03A settings.md)
├── Example configurations ─────────────────── → note 4 (links to anthropics/claude-code examples repo)
└── See also ───────────────────────────────── → notes 1/4/5 (links)
permission-modes.md
├── intro + Available modes (table) ────────── → note 5 (cc_permission_modes_overview)
├── Switch permission modes (per-interface) ── → note 5 (→ B03B CLI flags, B12 surfaces)
├── acceptEdits mode ───────────────────────── → note 6 (cc_permission_modes_detail)
├── plan mode (+ Review/approve, Set default) ─ → note 6 (→ B13B Ultraplan)
├── Eliminate prompts with auto mode ───────── → note 7 (cc_auto_mode)
│   ├── Enable on Bedrock/Vertex/Foundry ───── → note 7 (→ B14A providers)
│   ├── What the classifier blocks by default ─ → note 7
│   ├── Boundaries you state in conversation ── → note 7
│   └── When auto mode falls back ───────────── → note 7 (→ B17 error reference, B11 headless)
├── dontAsk mode ───────────────────────────── → note 6
├── bypassPermissions mode ─────────────────── → note 6
├── Protected paths (table + dirs/files) ───── → note 6
└── See also ───────────────────────────────── → notes 6/7/8 (links)
auto-mode-config.md
├── Where the classifier reads configuration ─ → note 8 (cc_auto_mode_configuration)
├── Define trusted infrastructure ──────────── → note 8
├── Override the block and allow rules ─────── → note 8
├── Inspect the defaults and effective config ─ → note 8
├── Review denials ─────────────────────────── → note 8 (→ B07 PermissionDenied hook)
└── See also ───────────────────────────────── → note 8 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| permissions (4,793w >2500, 12 H2) | notes 1,2,3,4 + link-outs | exceeds density cap; distinct concepts — rule model/syntax (1), per-tool dialects (2, long), hooks+working-dirs (3), managed-settings+precedence+sandbox (4); settings table / server-managed delivery / hook authoring owned by B03A/B14B/B07 |
| permission-modes (3,377w >2500, 9 H2) | notes 5,6,7 + link-outs | exceeds density cap; overview+switching (5) vs per-mode detail+protected-paths (6) vs the substantial auto-mode section (7) differ in scope; CLI flags / Ultraplan / providers / error-ref linked out |
| auto-mode (in permission-modes) + auto-mode-config (1,760w) | note 7 (concept) + note 8 (procedure) | the auto-mode concept (what/why/classifier behavior) and its configuration reference (`autoMode` settings + CLI subcommands) differ in BB (concept vs procedure); the two source sections are deliberately paired by the docs ("This page is the configuration reference") |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---|---:|---:|---|
| 1 | cc_permission_system_and_rules | concept | 650 | 2 | ✅ |
| 2 | cc_tool_specific_permission_rules | concept | 800 | 2 | ✅ |
| 3 | cc_permissions_hooks_and_working_directories | concept | 450 | 0 | ✅ |
| 4 | cc_managed_permission_settings_and_precedence | concept | 600 | 1 | ✅ |
| 5 | cc_permission_modes_overview | concept | 600 | 2 | ✅ |
| 6 | cc_permission_modes_detail | concept | 750 | 3 | ✅ |
| 7 | cc_auto_mode | concept | 700 | 2 | ✅ |
| 8 | cc_auto_mode_configuration | procedure | 600 | 5 | ✅ |

No note approaches the 2,500-word / 400-line caps; note 8 carries the most code (5 JSON/bash snippets) but stays ≤6. Note 2 is the largest at ~800w (still well under cap) because the source's tool-specific section is the densest. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_permission_system_and_rules cc_tool_specific_permission_rules cc_permissions_hooks_and_working_directories cc_managed_permission_settings_and_precedence cc_permission_modes_overview cc_permission_modes_detail cc_auto_mode cc_auto_mode_configuration"
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

Single phase (8 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from a vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (entry-point) | each note linked from `entry_claude_code_docs.md` (its 8 rows queued) so the cluster is reachable from the docs hub | entry-point row check at finalization |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under a "Permissions & access control" cluster + increments the BB-distribution counts (concept ×7, procedure ×1).

## Undigested Terms Plan (Step 4e)

b05a creates **no new `term_dictionary` notes** — every permissions-vocabulary term is covered by a b05a
`cc_` concept/procedure note, an existing substantive term note (link), or its home sub-plan (Pattern B):

| Term (page) | Disposition |
|---|---|
| Permission rule / allow-ask-deny (permissions) | note 1 `cc_permission_system_and_rules` (doc concept) |
| Permission mode (permission-modes) | note 5 `cc_permission_modes_overview` + link `term_graduated_trust` (exists) |
| Plan mode (permission-modes) | note 6 `cc_permission_modes_detail` (doc concept) |
| Auto mode / classifier (permission-modes, auto-mode-config) | note 7 `cc_auto_mode` + note 8 `cc_auto_mode_configuration` (doc concept/procedure) |
| Protected paths (permission-modes) | note 6 `cc_permission_modes_detail` (doc concept) |
| Working directories / additional directories (permissions) | note 3 `cc_permissions_hooks_and_working_directories` (doc concept) |
| Managed settings (permissions) | note 4 `cc_managed_permission_settings_and_precedence` (doc concept); delivery → B14B |
| Settings precedence / defaultMode (permissions, permission-modes) | note 4 / note 5; full settings reference → B03A `settings.md` |
| Sandboxing (permissions) | existing term note `term_sandbox` (link); mechanics → B05B `sandboxing.md` |
| Subagent / MCP / Compaction / Context window | existing term notes (link) |
| PreToolUse / PermissionRequest / PermissionDenied hook | owned by B07A/B07B (hooks) — captured there |
| Output style (Proactive) / Skill / Plugin / Channel | owned by home sub-plan (B06/B09/B08) — captured there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code for
newly-surfaced non-glossary terms. Surfaced candidates: **"deny-first / default deny"** (Manage permissions
evaluation order) → existing `term_deny_first` (link, NOT a new capture); **"protected paths"**,
**"acceptEdits / dontAsk / bypassPermissions modes"**, **"classifier" / "auto mode"** → all are
Claude-Code-specific feature vocabulary digested as `cc_` doc concepts (notes 6,7), not term_dictionary
terms (Pattern B). **0 new B05A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B05A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the page concepts duplicate existing notes?) was
performed: `term_graduated_trust`, `term_deny_first`, `term_sandbox`, `term_subagent`, `term_mcp`,
`term_access_control`, `term_human_in_the_loop`, `term_guardrails`, `term_values_over_rules`,
`term_reversibility_weighted_risk`, `term_contingent_authorization`, `term_function_calling` all exist →
linked, not recreated. No existing `cc_*` permission/auto-mode/mode doc note exists (dedup grep over

## Term-Note Authoring Requirements

**N/A for b05a** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (JSON `permissions`/`autoMode` config + `claude`/`bash` commands). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island, G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_graduated_trust.md` | notes 5, 6 | trust-spectrum term → CC permission-modes overview + per-mode detail (the canonical worked example) |
| `term_dictionary/term_deny_first.md` | notes 1, 4 | deny-first pattern term → CC allow/ask/deny rule model + managed-settings deny precedence |
| `term_dictionary/term_sandbox.md` | note 4 | sandbox term → CC permissions × sandboxing complementary-layers section |
| `term_dictionary/term_claude_code.md` | notes 1, 5, 7 | product term → CC permission system / modes / auto mode |
| `term_dictionary/term_guardrails.md` | note 7 | guardrails term → CC auto-mode classifier as runtime guardrail |
| `0_entry_points/entry_claude_code_docs.md` | notes 1–8 (8 rows) | docs hub → all B05A notes (G8) |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8 rows for `entry_claude_code_docs.md` under a "Permissions & access control" cluster; `/tessellum-check-broken-links`.
- Add forward cross-links from B05B sandboxing notes (sandbox × permissions), B07 hooks notes (PreToolUse/PermissionRequest/PermissionDenied), and B16 security notes (defense-in-depth) into this cluster once those sub-plans execute.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B05A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/`; measured words match the master's figures (permissions 4,793 · permission-modes 3,377 · auto-mode-config 1,760 = 9,930). No >1.5× under-estimate; the two large pages (permissions 4.8Kw, permission-modes 3.4Kw) forced documented splits, both >2,500-word cap.
- **Notes**: 8 (concept 7, procedure 1) — matches master estimate. Splits documented in Split Decisions; auto-mode concept (note 7) separated from its config reference (note 8) on a BB boundary (concept vs procedure).
- **Step 2d new-term scan**: candidates surfaced (deny-first, protected paths, mode names, classifier) → `term_deny_first` linked (exists), the rest are CC-specific feature vocabulary digested as `cc_` doc concepts; **0 new B05A term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), Section Coverage Map, Split Decisions, Density Re-Assessment, Inlinks table, G7/G8 gate rows.
- **28-item checklist**: PASS (term-note items N/A — B05A authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), including G7 inbound-link and G8 entry-point discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B05A contributes 8 rows under a Permissions cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes) exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–800w, ≤5 code — none borderline; the two >2,500-word source pages already split into 4 + 3 notes. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: permissions 4,793 = plan 4,793; permission-modes 3,377 = plan 3,377; auto-mode-config 1,760 = plan 1,760. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B05A authors 0 term notes; Undigested Terms Plan routes every page term (link existing / cc_ doc / home sub-plan); Authoring Requirements inherited from master. |
| CP9 | Discoverability (G7/G8 inlinks executed) | ✅ PASS | Inlinks table provides ≥1 inbound link per note from outside `claude_code/` (term notes + entry-point hub), executed at finalization with DB in-degree ≥1 verification. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
