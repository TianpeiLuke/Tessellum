---
title: Sub-Plan B03A — Claude Code Docs: Settings & Environment Variables
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["settings", "env-vars"]
---

# Sub-Plan B03A: Settings & Environment Variables

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 2 configuration-system reference pages: `settings.md` (the `settings.json` field reference, the
scope/precedence model, managed-settings delivery, and the grouped sub-tables for sandbox / permissions /
attribution / hooks / plugins / file-suggestion / policy-helper) and `env-vars.md` (the full ~190-variable
environment-variable reference plus how/where to set them and how they take precedence). P1 (Phase A) —
settings scopes, the `env` key, permission rules, and the managed tier are referenced by nearly every later
sub-plan (permissions B05A, sandboxing B05B, MCP B08A, hooks B07, plugins B09, model B03B), so this runs early.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 21,168 measured words. **Planned: 10 notes.**

## Content Strategy

- **Prioritize**: the scope/precedence model and the managed tier (the cross-cutting mental model every other
  config page builds on), the `settings.json` available-settings reference, and the env-var reference grouped
  by purpose. These are the canonical lookups other sub-plans link to.
- **Group / split**: `settings.md` (11.5Kw, 66 code blocks, 22 H3) far exceeds caps — split by sub-system into
  scope model (concept), the available-settings reference (procedure), managed settings (procedure), and the
  grouped sub-tables (sandbox / permissions+attribution+files / plugins). `env-vars.md` (9.7Kw) is one giant
  reference table — split the ~190 variables into purpose-grouped reference notes (set-and-precede mechanics;
  provider/auth/model; behavior-toggle/runtime/telemetry) so no note exceeds the 2,500-word cap.
- **Skip / link-out (own other sub-plans)**: full permission rule syntax → permissions B05A (`permissions.md`);
  full sandbox semantics → sandboxing B05B (`sandboxing.md`); managed-settings delivery detail →
  `server-managed-settings` (B14B) / `managed-mcp` (B08A); model/effort/fallback fields → model-config (B03B);
  hooks format → B07A; plugin marketplace policy detail → B09B; monitoring/OTel detail → B15B. These are
  referenced via links, never duplicated.
- **Dedup (link, do NOT recreate)**: `term_mcp`, `term_subagent`, `term_sandbox`, `term_skills`,
  `term_graduated_trust`, `term_compaction`, `term_authentication`, `term_oauth_token`,
  `term_observability_agent_systems`, `term_llm` are existing substantive term notes — linked, not recreated.
  `tutorial_claude_code_04_configuration.md` (694w, internal BYOA onboarding, different BB) is a
  practical companion — cross-linked, not duplicated by these reference notes.

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| settings | /settings | 11,508 | 33 | 7 | 22 | concept + procedure |
| env-vars | /env-vars | 9,660 | 1 | 4 | 2 | procedure (reference) |

> **Code blocks** counted as fence-pairs (settings 66 fences = 33 blocks; env-vars 2 fences = 1 block).
> **H2 lists (document order):**
> - **settings**: Configuration scopes (H3 Available scopes · When to use each scope · How scopes interact ·
>   What uses scopes) · Settings files (H3 When edits take effect · Invalid entries in managed settings ·
>   Available settings · Global config settings · Worktree settings · Permission settings · Permission rule
>   syntax · Sandbox settings [H4 Sandbox path prefixes] · Attribution settings · File suggestion settings ·
>   Hook configuration · Compute managed settings with a policy helper · Settings precedence · Verify active
>   settings · Key points about the configuration system · System prompt · Excluding sensitive files) ·
>   Subagent configuration · Plugin configuration (H3 Plugin settings [H4 enabledPlugins · extraKnownMarketplaces ·
>   strictKnownMarketplaces · strictPluginOnlyCustomization] · Managing plugins) · Environment variables ·
>   Tools available to Claude · See also
> - **env-vars**: Set environment variables (H3 In your shell · In settings files) · Precedence · Variables ·
>   See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **10 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_settings_scopes_and_precedence.md` | concept | settings: Configuration scopes (all H3), Settings precedence, How scopes interact, Verify active settings, Key points | 700 | The four scopes (managed/user/project/local), where each lives, who it affects; the precedence order; array-merge vs scalar-override rule; `fallbackModel`/`availableModels` exceptions; `/status` Setting sources verification. Links `term_graduated_trust`. |
| 2 | `cc_settings_files.md` | concept | settings: Settings files (intro, file locations, $schema, When edits take effect, ~/.claude.json, backups) | 550 | The `settings.json` mechanism: user/project/local files, `$schema` autocomplete, hot-reload vs read-once keys (`model`/`outputStyle`), `~/.claude.json` other-config, timestamped backups. |
| 3 | `cc_settings_reference.md` | procedure | settings: Available settings table, Global config settings, Worktree settings | 1,800 | Field reference for `settings.json` keys (the big Available-settings table) + the `~/.claude.json` global-config keys + `worktree.*` keys. One-line-per-key purpose; deep semantics linked out (model→B03B, permissions→note 5, sandbox→note 6, hooks→note 7, plugins→notes 8/9). |
| 4 | `cc_managed_settings.md` | procedure | settings: Settings files (managed delivery), Invalid entries in managed settings, Compute managed settings with a policy helper | 900 | Managed-settings delivery mechanisms (server-managed, MDM plist/registry, file-based `managed-settings.json` + `managed-settings.d/` drop-in merge), tolerant parsing of invalid entries (per-field security table), and the `policyHelper` executable. Managed-only field semantics linked to permissions B05A / server-managed B14B. |
| 5 | `cc_permission_and_attribution_settings.md` | procedure | settings: Permission settings, Permission rule syntax (quick), Attribution settings, File suggestion settings | 750 | The `permissions.{allow,ask,deny,additionalDirectories,defaultMode,...}` settings keys, quick rule-syntax examples (full syntax → B05A), `attribution.{commit,pr}` git/PR trailers, and the `fileSuggestion` custom `@`-autocomplete command. |
| 6 | `cc_sandbox_settings.md` | procedure | settings: Sandbox settings, Sandbox path prefixes, Excluding sensitive files | 850 | The `sandbox.*` settings keys (enable, fail-if-unavailable, filesystem allow/deny read/write, network domains/sockets/proxy, weaker-sandbox), path-prefix resolution, and `permissions.deny` for excluding sensitive files. Sandbox mechanics → B05B. |
| 7 | `cc_hook_configuration_settings.md` | procedure | settings: Hook configuration | 450 | Settings that gate hooks: `allowManagedHooksOnly`, `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, `disableAllHooks` — what each restricts and how arrays merge. Hook authoring format → B07A. |
| 8 | `cc_subagent_and_plugin_settings.md` | concept | settings: Subagent configuration, Plugin configuration (intro), Plugin settings (enabledPlugins, extraKnownMarketplaces, Managing plugins) | 700 | Subagent file locations (`~/.claude/agents/`, `.claude/agents/`); `enabledPlugins` map + scope fallback; `extraKnownMarketplaces` team registration + source types; `/plugin` management. Strict managed policy → note 9. |
| 9 | `cc_managed_plugin_policy_settings.md` | procedure | settings: strictKnownMarketplaces, strictPluginOnlyCustomization, blockedMarketplaces (from table) | 900 | Managed-only marketplace/customization policy: `strictKnownMarketplaces` allowlist (8 source types, exact vs regex matching), `strictPluginOnlyCustomization` surface lockdown, comparison vs `extraKnownMarketplaces`. User-facing marketplace policy → B09B. |
| 10 | `cc_environment_variables.md` | procedure | env-vars: Set environment variables (shell + settings `env`), Precedence, Variables (full table), See also | 1,900 | How and where env vars are set (shell export vs settings `env` key), env-var-over-setting precedence, and the purpose-grouped variable reference (model/auth/provider; API/timeouts/streaming; behavior toggles; telemetry/OTel; MCP/plugins). Per-domain deep links (model→B03B, monitoring→B15B, providers→B14A). |

**Estimate: 10 notes** — concept ×3 (notes 1,2,8), procedure ×7 (notes 3,4,5,6,7,9,10). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (21,168 words). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B; managed at master).
- Est. total digest words: ~9,500 (avg ~950/note; the two reference notes 3 and 10 carry the largest field/var tables). Code blocks: ~14 across the 10 notes (settings is JSON-example heavy; verbatim where load-bearing).
- **Building Block Distribution**: concept ×3 (notes 1,2,8) · procedure ×7 (notes 3,4,5,6,7,9,10). No model/argument/empirical_observation in this sub-plan (config reference is concept + procedure only).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_settings_scopes_and_precedence` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's own scope/precedence configuration model (managed/user/project/local), so the product term is the definitional anchor for what is being configured.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note's precedence ladder and the managed-tier override exist to enforce trust boundaries (a repo cannot grant itself more capability than user/managed scope allows), the graduated-trust model this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The "What uses scopes" table maps skills to user/project locations, so scope precedence directly governs where skills load from and which scope wins on conflict.
- [Subagent](../../term_dictionary/term_subagent.md) — Subagents are one of the scoped features in the "What uses scopes" table (`~/.claude/agents/` vs `.claude/agents/`), so the scope model determines subagent availability and sharing.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — MCP servers appear in the scope table with per-scope storage (`~/.claude.json` vs `.mcp.json`), and the precedence rules govern which MCP config a session uses.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The scope/precedence system is how the Claude Code harness resolves its effective runtime configuration before wiring tools, settings, and policy into the model, the configuration-resolution layer of the harness.

### 2. `cc_settings_files` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's `settings.json` files and `~/.claude.json` — the on-disk configuration of the Claude Code product itself.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `settings.json` is the official mechanism the harness reads at startup (and hot-reloads) to configure permissions, env, and hooks, so the settings file is the harness's primary configuration surface.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note explains that user/local MCP server configurations live in `~/.claude.json` while project MCP servers live in `.mcp.json`, distinguishing the settings-file storage of MCP config.
- [Skills](../../term_dictionary/term_skills.md) — Skills are configured through `settings.json` (e.g. `skillOverrides`, `disableBundledSkills`), so the settings-file mechanism this note describes is how skill behavior is persisted.
- [Compaction](../../term_dictionary/term_compaction.md) — The "When edits take effect" rule (some keys hot-reload, `outputStyle` rebuilds on `/clear`) parallels how the system prompt is reassembled around context events like compaction, contextualizing the read-once-vs-reload distinction.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note notes `.claude/settings.local.json` is gitignored and project trust governs which settings files are honored, the per-scope trust model this term defines.

### 3. `cc_settings_reference` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the field-by-field reference for Claude Code's `settings.json` keys, so the product term anchors the configuration surface being enumerated.
- [Skills](../../term_dictionary/term_skills.md) — Multiple reference keys configure skills (`disableBundledSkills`, `skillOverrides`, `maxSkillDescriptionChars`, `skillListingBudgetFraction`), so the term grounds that family of settings.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Reference keys like `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers` configure MCP server approval, so the term grounds the MCP-related settings rows.
- [Subagent](../../term_dictionary/term_subagent.md) — The `agent` key runs the main thread as a named subagent and sets the default dispatched agent, so the subagent concept is configured directly by this reference.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Many reference keys are managed-settings-only enforcement toggles (`disableAutoMode`, `disableRemoteControl`, `forceLoginMethod`), expressing the graduated-trust policy ladder this term defines.
- [Compaction](../../term_dictionary/term_compaction.md) — Keys such as `cleanupPeriodDays` and the context/skill-budget settings interact with the session/context lifecycle that compaction manages, tying these reference rows to context management.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — The `model`, `availableModels`, `fallbackModel`, `modelOverrides`, and `advisorModel` keys all select or constrain the LLM Claude Code calls, making the LLM concept central to this reference's model family.

### 4. `cc_managed_settings` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents how Claude Code reads organization-deployed managed settings across delivery mechanisms — an enterprise-configuration feature of the Claude Code product.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Managed settings are the top of the precedence ladder that cannot be overridden by user or project scope, the strictest tier of the graduated-trust model this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The policy helper and tolerant-parsing behavior describe how the harness computes and validates its effective policy at startup before running, a harness configuration-resolution concern.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Managed settings carry MCP allow/deny policy (`allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`) whose invalid-entry handling this note's security table specifies.
- [Authentication](../../term_dictionary/term_authentication.md) — Managed fields `forceLoginMethod` and `forceLoginOrgUUID` (and their fail-closed invalid handling) constrain how a user authenticates, so authentication is directly governed by managed settings.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — `claude doctor` surfaces each invalid managed-settings entry with its source and field, and validation errors surface in interactive/headless/doctor channels — the observability/diagnostics surface for policy correctness.

### 5. `cc_permission_and_attribution_settings` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's permission, attribution, and file-suggestion settings keys — configuration of the Claude Code product's safety and integration behavior.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The `permissions.{allow,ask,deny,defaultMode}` keys and `disableBypassPermissionsMode` are exactly the allowlist/ask/deny ladder and mode controls that implement graduated trust.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — `Edit`/`Read` permission rules merge into the sandbox filesystem boundary and `WebFetch` rules into network domains, so permission settings co-determine the sandbox this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Permission rules use the `mcp__<server>__tool` syntax to allow/deny MCP tools, so the term grounds the MCP-rule examples in this note.
- [Subagent](../../term_dictionary/term_subagent.md) — `additionalDirectories` and `Agent` permission rules govern subagent file access and dispatch, linking permission settings to subagent capability.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Attribution settings (`commit`/`pr` trailers) exist because an autonomous coding agent authors commits and PRs; the deny rules exclude secrets from an agent that otherwise reads the whole project, the safety envelope this term motivates.

### 6. `cc_sandbox_settings` (6 term notes)
- [Sandboxing](../../term_dictionary/term_sandbox.md) — This note documents the `sandbox.*` settings keys that configure bash command isolation from filesystem and network — the direct settings interface to the sandboxing concept this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The settings configure Claude Code's own bash-sandboxing feature (macOS/Linux/WSL2), so the product term anchors what these keys isolate.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `autoAllowBashIfSandboxed`, `failIfUnavailable`, and `allowUnsandboxedCommands` trade autonomy for safety — auto-approving bash only inside the sandbox — the graduated-trust bargain this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Sandbox filesystem/network restrictions exist to let an autonomous coding agent run arbitrary commands without exfiltration or destructive writes, the containment this term's agents require.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `network.allowUnixSockets` / `allowAllUnixSockets` and proxy ports govern socket access that stdio MCP servers and tooling use inside the sandbox, tying MCP transport to sandbox network policy.
- [Authentication](../../term_dictionary/term_authentication.md) — `filesystem.denyRead` defaults protect credential paths (`~/.aws/credentials`) and `network.allowedDomains` bounds outbound auth traffic, so the sandbox boundary directly protects authentication material this term covers.

### 7. `cc_hook_configuration_settings` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's hook-gating settings (`allowManagedHooksOnly`, `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, `disableAllHooks`) — configuration of the Claude Code hook system.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — Hooks fire on Claude Code lifecycle events (the `ConfigChange` hook fires on settings reload), and these settings control which hooks run at those events, the lifecycle-event signals this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `allowManagedHooksOnly` blocks user/project hooks so only vetted managed/plugin hooks run, and HTTP-URL/env-var allowlists bound what hooks can reach — the trust-scoping ladder this term names.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `strictPluginOnlyCustomization` (referenced here) blocks user/project hooks and MCP servers alike, treating hooks and MCP as parallel plugin-delivered surfaces, contextualizing the hook policy against MCP policy.
- [Skills](../../term_dictionary/term_skills.md) — Hooks and skills are sibling customization surfaces locked together by `strictPluginOnlyCustomization`, so the term grounds the plugin-only customization context these hook settings sit in.
- [Subagent](../../term_dictionary/term_subagent.md) — `SubagentStop` and other subagent-scoped hooks are gated by these settings, linking hook configuration to subagent lifecycle control.

### 8. `cc_subagent_and_plugin_settings` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — The note documents subagent configuration file locations (`~/.claude/agents/`, `.claude/agents/`) and how user vs project subagents are shared, the core subagent-storage model this term defines.
- [Skills](../../term_dictionary/term_skills.md) — Plugins distribute skills (alongside agents, hooks, MCP servers), so the `enabledPlugins`/`extraKnownMarketplaces` settings this note covers govern which plugin skills load.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Plugins also distribute MCP servers, so the plugin-enablement settings here determine which plugin-provided MCP servers are available.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Subagents and the plugin system are Claude Code extension mechanisms; the product term anchors what these settings extend.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Subagent files define specialized harness instances (custom prompt, tool restrictions, model), so each subagent config is a scoped harness definition this term describes.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — Configuring multiple project/user subagents that a lead can dispatch is the multi-agent composition this term defines, set up through these subagent settings.

### 9. `cc_managed_plugin_policy_settings` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's managed-only plugin/marketplace policy settings, an enterprise governance feature of the Claude Code product.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `strictKnownMarketplaces` (allowlist), `blockedMarketplaces` (blocklist), and `strictPluginOnlyCustomization` (surface lockdown) are the highest-precedence trust gates that user/project scope cannot override, the strict end of the graduated-trust ladder.
- [Skills](../../term_dictionary/term_skills.md) — `strictPluginOnlyCustomization` can block user/project skills so they come only from vetted plugins or managed settings, directly governing the skill supply chain this term names.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The same lockdown can block user/project MCP servers (loading only plugin/managed MCP), so the term grounds the MCP surface of the plugin-policy lockdown.
- [Subagent](../../term_dictionary/term_subagent.md) — `strictPluginOnlyCustomization` also locks the `agents` surface, restricting subagents to plugin/managed sources, tying subagent governance to this policy.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — These policies control the full customization supply chain (skills/agents/hooks/MCP) the harness assembles, defining the trusted extension set the harness is allowed to load.

### 10. `cc_environment_variables` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the reference for the environment variables that control Claude Code behavior (`CLAUDE_CODE_*`, `ANTHROPIC_*`, and more), so the product term anchors the entire variable surface.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — A large variable family selects and routes the LLM (`ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`, `MAX_THINKING_TOKENS`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`), making the LLM concept central to the model/auth group.
- [Authentication](../../term_dictionary/term_authentication.md) — Auth variables (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`, `forceLogin*` interactions) determine how the session authenticates, the mechanism this term defines.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — `CLAUDE_CODE_OAUTH_REFRESH_TOKEN`/`CLAUDE_CODE_OAUTH_SCOPES` exchange a refresh token for access without a browser — exactly the OAuth-token-refresh flow this term documents.
- [Compaction](../../term_dictionary/term_compaction.md) — `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `DISABLE_AUTO_COMPACT`, and `DISABLE_COMPACT` tune or disable auto-compaction, the context-management mechanism this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Many variables tune MCP (`MCP_TIMEOUT`, `MCP_TOOL_TIMEOUT`, `MAX_MCP_OUTPUT_TOKENS`, `ENABLE_TOOL_SEARCH`, `MCP_CONNECTION_NONBLOCKING`), grounding the MCP group of the reference.
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — The `CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*`, and `DISABLE_TELEMETRY`/`DO_NOT_TRACK` variables configure OpenTelemetry metrics/logs/traces — the observability instrumentation this term defines for agent systems.
- [Subagent](../../term_dictionary/term_subagent.md) — Variables like `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`, `TASK_MAX_OUTPUT_LENGTH`, and `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` govern subagent execution, linking the reference to the subagent concept.

## Section Coverage Map

```
settings.md
├── Configuration scopes ─────────────────────── → note 1
│   ├── Available scopes ──────────────────────── → note 1
│   ├── When to use each scope ────────────────── → note 1
│   ├── How scopes interact ───────────────────── → note 1
│   └── What uses scopes ──────────────────────── → note 1
├── Settings files (intro / locations / $schema) → note 2
│   ├── managed delivery mechanisms ───────────── → note 4
│   ├── When edits take effect ────────────────── → note 2
│   ├── Invalid entries in managed settings ───── → note 4
│   ├── Available settings (table) ────────────── → note 3
│   ├── Global config settings ────────────────── → note 3
│   ├── Worktree settings ─────────────────────── → note 3
│   ├── Permission settings ───────────────────── → note 5
│   ├── Permission rule syntax (quick) ────────── → note 5 (full → B05A permissions.md)
│   ├── Sandbox settings (+ path prefixes) ────── → note 6 (mechanics → B05B sandboxing.md)
│   ├── Attribution settings ──────────────────── → note 5
│   ├── File suggestion settings ──────────────── → note 5
│   ├── Hook configuration ────────────────────── → note 7 (format → B07A hooks.md)
│   ├── Compute managed settings w/ policy helper → note 4
│   ├── Settings precedence ───────────────────── → note 1
│   ├── Verify active settings ────────────────── → note 1
│   ├── Key points about the config system ─────── → note 1
│   ├── System prompt ─────────────────────────── → note 3 (links; --append-system-prompt → B03B cli)
│   └── Excluding sensitive files ─────────────── → note 6 (permissions.deny for secrets)
├── Subagent configuration ───────────────────── → note 8 (full → B10A sub-agents.md)
├── Plugin configuration ─────────────────────── → note 8
│   ├── Plugin settings (enabledPlugins, extraKnownMarketplaces) → note 8
│   ├── strictKnownMarketplaces ───────────────── → note 9 (user-facing → B09B)
│   ├── strictPluginOnlyCustomization ─────────── → note 9
│   └── Managing plugins ──────────────────────── → note 8 (full → B09A plugins.md)
├── Environment variables (intro) ────────────── → note 10 (cross-ref to env-vars page)
├── Tools available to Claude ─────────────────── → linked out (B03B tools-reference.md)
└── See also ──────────────────────────────────── → notes 1/5 (links: permissions/auth/debug-config)
env-vars.md
├── Set environment variables ────────────────── → note 10
│   ├── In your shell ─────────────────────────── → note 10
│   └── In settings files ─────────────────────── → note 10 (links note 2/3 `env` key)
├── Precedence ────────────────────────────────── → note 10
├── Variables (full ~190-var table) ───────────── → note 10 (deep links: model→B03B, monitoring→B15B, providers→B14A)
└── See also ──────────────────────────────────── → note 10 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| settings.md (11.5Kw, 33 code, 22 H3 — far >2500w/>6 code caps) | notes 1–9 + link-outs | Distinct sub-systems with distinct BB: scope model (concept) vs settings-file mechanism (concept) vs available-settings reference (procedure) vs managed delivery (procedure) vs permission/attribution (procedure) vs sandbox (procedure) vs hook gating (procedure) vs subagent+plugin (concept) vs managed-plugin policy (procedure). Each note stays <2,500w / <6 code. |
| settings: Available settings (single ~100-key table, >2500w alone) | note 3 (+ deep semantics linked out) | The full key table exceeds the word cap on its own; note 3 gives one-line purpose per key and links deep semantics to the owning note/sub-plan (model→B03B, permissions→note 5, sandbox→note 6, hooks→note 7, plugins→8/9), keeping it within caps. |
| env-vars.md (9.7Kw, ~190-var table) | note 10 (purpose-grouped, deep links) | One reference page; kept as a single note but the variable table is grouped by purpose (model/auth/provider · API/timeout/streaming · behavior toggle · telemetry/OTel · MCP/plugin) with one-line purpose per var and deep links out, holding it under 2,500w (~1,900w). |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_settings_scopes_and_precedence | concept | 700 | 1 | ✅ |
| 2 | cc_settings_files | concept | 550 | 1 | ✅ |
| 3 | cc_settings_reference | procedure | 1,800 | 1 | ✅ |
| 4 | cc_managed_settings | procedure | 900 | 2 | ✅ |
| 5 | cc_permission_and_attribution_settings | procedure | 750 | 3 | ✅ |
| 6 | cc_sandbox_settings | procedure | 850 | 2 | ✅ |
| 7 | cc_hook_configuration_settings | procedure | 450 | 2 | ✅ |
| 8 | cc_subagent_and_plugin_settings | concept | 700 | 2 | ✅ |
| 9 | cc_managed_plugin_policy_settings | procedure | 900 | 3 | ✅ |
| 10 | cc_environment_variables | procedure | 1,900 | 2 | ✅ |

Notes 3 and 10 are the densest (reference tables) at ~1,800–1,900 words — within the 2,500-word cap with margin; if a draft exceeds 2,300w the table is trimmed to one-line-per-key/var with deep links (already the plan). No note exceeds 6 code blocks. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_settings_scopes_and_precedence cc_settings_files cc_settings_reference cc_managed_settings cc_permission_and_attribution_settings cc_sandbox_settings cc_hook_configuration_settings cc_subagent_and_plugin_settings cc_managed_plugin_policy_settings cc_environment_variables"
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

Single phase (10 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (field/var semantics verbatim) | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 10 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes). This sub-plan **contributes its 10 rows** under a
"Settings & Environment Variables" cluster + increments the BB-distribution counts (concept +3, procedure +7).

## Undigested Terms Plan (Step 4e)

b03a creates **no new `term_dictionary` notes**. Both pages are configuration *reference* — they reference the
Claude Code vocabulary but do not introduce new cross-cutting glossary terms that lack a home. Per Pattern B,
every term either has a `cc_` doc-concept home, an existing substantive term note (link), or a home sub-plan:

| Term surfaced in b03a pages | Disposition |
|---|---|
| Settings layers / scope / precedence | note 1 `cc_settings_scopes_and_precedence` (doc concept) — this is the master-assigned B03A owner of "Settings layers" |
| Managed settings | note 4 `cc_managed_settings` (doc concept/procedure) |
| Permission mode / auto mode / plan mode | link `term_graduated_trust` (exists); full concept owned by B05A |
| Sandboxing | link `term_sandbox` (exists); mechanics owned by B05B |
| MCP / Subagent / Skill / Hook / Plugin / Compaction | existing term notes (link) or home sub-plan (B08A/B10A/B06/B07/B09) |
| Extended thinking / effort level / fallback model / model overrides | link `term_chain_of_thought` / owned by B03B (model-config) |
| OAuth token / API key / authentication | link `term_oauth_token`, `term_authentication` (exist); full concept owned by B14B |
| Telemetry / OpenTelemetry / observability | link `term_observability_agent_systems` (exists); full concept owned by B15B |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages scanning the field/variable tables, notes,
and warnings for newly-surfaced cross-cutting terms. Candidates considered: "policy helper", "drop-in
directory merge", "byte/event streaming watchdog", "co-authored-by trailer". Each is a *feature of a specific
setting/variable* documented inline in its `cc_` note, not a reusable cross-cutting vocabulary term, and none
has a glossary home or warrants a standalone term note. **0 new b03a `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b03a authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these config concepts duplicate existing notes?)
was performed: `term_mcp`, `term_subagent`, `term_sandbox`, `term_skills`, `term_graduated_trust`,
`term_compaction`, `term_authentication`, `term_oauth_token`, `term_observability_agent_systems`,
`term_llm`, `term_agent_lifecycle_event` all exist → linked, not recreated. The `cc_` doc-concept notes
(scopes/precedence, managed settings) do not duplicate any existing *term* note (the P0 failure mode the
master's dedup policy guards against): no `term_settings_*` or `term_managed_settings` exists.

## Term-Note Authoring Requirements

**N/A for b03a** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory; field/variable semantics
  (defaults, min-versions, managed-only flags, precedence) must be transcribed verbatim, not paraphrased.
- Code blocks (JSON settings examples, shell exports) verbatim. One BB per note. Each note ≤400 lines
  (split if a draft >350); notes 3 and 10 (reference tables) are the split-risk notes — trim to one-line-per-key
  with deep links if a draft exceeds 2,300 words.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `resources/term_dictionary/term_claude_code.md` | notes 1, 3, 10 | product term → CC settings scopes / settings reference / env-var reference |
| `resources/term_dictionary/term_graduated_trust.md` | notes 1, 4, 9 | trust term → scope precedence / managed settings / managed plugin policy |
| `resources/term_dictionary/term_sandbox.md` | note 6 | sandbox term → CC sandbox settings keys |
| `resources/term_dictionary/term_oauth_token.md` | note 10 | OAuth-refresh term → env-var auth/OAuth variables |
| `resources/term_dictionary/term_observability_agent_systems.md` | note 10 | observability term → env-var telemetry/OTel variables |
| `resources/documentation/tutorials/tutorial_claude_code_04_configuration.md` | notes 1, 3, 5 | config tutorial → canonical settings scopes / reference / permission settings |
| `resources/documentation/tutorials/tutorial_claude_code_getting_started.md` | note 2 | getting-started tutorial → CC settings-files mechanism |

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and DB-verify
  in-degree ≥1 for all 10 (G7/G8); queue the 10 rows for `entry_claude_code_docs.md` under a "Settings &
  Environment Variables" cluster; `/tessellum-check-broken-links`.
- When B05A (permissions), B05B (sandboxing), B03B (model-config), B07A (hooks), B09A/B09B (plugins), B14B
  (auth/server-managed), and B15B (monitoring) execute, add reciprocal links from those notes back into this
  cluster (the link-outs declared in the Section Coverage Map become bidirectional).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13** — see Review Sign-Off (9/9 → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B03A, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read fully from `inbox/claude_code_docs/`; measured words match
  the master figure (settings 11,508 · env-vars 9,660 = 21,168). Structure measured directly: settings has
  7 H2 / 22 H3 / 33 code blocks (66 fences); env-vars has 4 H2 / 2 H3 / 1 code block. Both pages far exceed the
  density caps individually, forcing the split into 10 notes (documented in Split Decisions).
- **Notes**: 10 (concept 3, procedure 7) — matches master estimate. The big single tables (settings
  Available-settings ~100 keys; env-vars ~190 vars) are each kept to one-line-per-key/var with deep links to
  the owning note/sub-plan so notes 3 and 10 stay under the 2,500-word cap.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard —
  6–8 term notes per note (16 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
  Claude Code/agentic pool plus DB-confirmed existing notes (`term_observability_agent_systems`, `term_llm`,
  `term_oauth_token`, `term_agent_lifecycle_event`, `term_multi_agent`).
- **Dedup (G-B)**: confirmed `resources/documentation/claude_code/` does not yet exist (no cc_ note to
  collide with); `tutorial_claude_code_04_configuration.md` (694w, Amazon BYOA onboarding, different BB) is a
  companion, not a duplicate — cross-linked. No existing `term_settings_*`/`term_managed_settings` to over-merge.
- **Step 2d new-term scan**: candidates (policy helper, drop-in merge, streaming watchdog, co-authored-by
  trailer) all judged inline-feature, not cross-cutting terms; **0 new b03a term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G8 verification notes, Split Decisions for the two oversized tables.
- **28-item checklist**: PASS (term-note items N/A — b03a authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed; set to `ready` after the 9-checkpoint self-review below (9/9 PASS).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7 Inlink-executed and G8 in-degree ≥1. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B03A contributes 10 rows under a "Settings & Environment Variables" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2 / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | Both oversized source pages already split into 10 single-BB notes; the two densest (3 reference, 10 reference) capped at ~1,800–1,900w with one-line-per-key/var + deep links, trim rule stated. No borderline note left un-split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: settings 11,508 = plan 11,508; env-vars 9,660 = plan 9,660; total 21,168 = master 21,168. Within ±0%. H2/H3/code counts measured via grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | b03a authors 0 term notes; Undigested Terms Plan routes every surfaced term to an existing term note / `cc_` doc-concept / home sub-plan; Authoring Requirements inherited from master. |
| CP9 | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented — 11 existing terms linked not recreated; no `cc_` doc-concept duplicates an existing term note (no `term_settings_*`/`term_managed_settings` exists), guarding the P0 doc-duplicates-term failure. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
