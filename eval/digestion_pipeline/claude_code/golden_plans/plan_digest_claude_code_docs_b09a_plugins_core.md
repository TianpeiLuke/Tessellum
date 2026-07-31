---
title: Sub-Plan B09A — Claude Code Docs: Plugins Core
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["plugins", "plugins-reference", "discover-plugins"]
---

# Sub-Plan B09A: Plugins Core

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md),
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 plugin-system pages that define what a Claude Code plugin is, how to create one, the complete
technical reference (manifest schema, component types, CLI, caching, versioning), and how to discover and
install plugins through marketplaces. P2 (Phase B) — plugins build on the cores already digested by Phase A
(skills B06, hooks B07, MCP B08, subagents B10), which this sub-plan links rather than re-defines.
Plugin **marketplace creation** and **dependency resolution** are owned by the sibling sub-plan B09B
(`plugin-marketplaces.md`, `plugin-dependencies.md`, `plugin-hints.md`) and are linked, not duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 14,190 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the plugin definition, the directory/manifest structure, and the install/marketplace flow — the load-bearing concepts every later plugin reference links (P2).
- **Group**: split the large `plugins-reference` (8,257 w, 10 H2 / 41 H3) by sub-concern — components reference vs manifest schema vs caching/versioning vs CLI vs debugging — each its own BB-atomic note. Keep the `plugins` guide split into overview (concept) vs quickstart/migration (procedure). Keep `discover-plugins` as the install/marketplace procedure note plus its catalog (concept).
- **Skip / link-out (own other sub-plans)**: marketplace creation + `marketplace.json` schema → B09B (`plugin-marketplaces`); dependency `dependencies` field + version resolution + `plugin tag` semantics + `plugin prune` rationale → B09B (`plugin-dependencies`); CLI plugin hints / `pluginSuggestionMarketplaces` recommendation → B09B (`plugin-hints`); skill authoring detail → B06 (`skills`); subagent config detail → B10A (`sub-agents`); hook event semantics → B07A (`hooks`); MCP server config detail → B08A (`mcp`); settings/scope precedence detail → B03A (`settings`); managed marketplace restrictions → B14B (`server-managed-settings`). Referenced via links, never duplicated.
- **Terms**: not re-digested into new `term_dictionary` notes — plugin vocabulary routes to existing term notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| plugins | /plugins | 2,973 | 10 | 7 | 15 | concept/procedure |
| plugins-reference | /plugins-reference | 8,257 | 33 | 10 | 41 | concept/procedure |
| discover-plugins | /discover-plugins | 2,960 | 22 | 12 | 16 | procedure/concept |

> **H2 lists (document order):**
> - **plugins**: When to use plugins vs standalone configuration · Quickstart (H3 Prerequisites, Create your first plugin) · Develop a plugin in your skills directory · Plugin structure overview · Develop more complex plugins (H3 Add Skills, Add LSP servers, Add background monitors, Ship default settings, Organize complex plugins, Test your plugins locally, Debug plugin issues, Share your plugins, Submit your plugin to the community marketplace) · Convert existing configurations to plugins (H3 Migration steps, What changes when migrating) · Next steps (H3 For plugin users, For plugin developers)
> - **plugins-reference**: Plugin components reference (H3 Skills, Agents, Hooks, MCP servers, LSP servers, Monitors, Themes) · Plugin installation scopes · Skills-directory plugins (H3 Choose where the plugin loads from, Edit/reload/disable) · Plugin manifest schema (H3 Complete schema, Required fields, Unrecognized fields, Metadata fields, Default enablement, Component path fields, Experimental components, User configuration, Channels, Path behavior rules, Environment variables) · Plugin caching and file resolution (H3 Path traversal limitations, Share files with symlinks) · Plugin directory structure (H3 Standard plugin layout, File locations reference) · CLI commands reference (H3 plugin init/install/uninstall/prune/enable/disable/update/list/details/tag) · Debugging and development tools (H3 Debugging commands, Common issues, Example error messages, Hook troubleshooting, MCP server troubleshooting, Directory structure mistakes) · Distribution and versioning reference (H3 Version management) · See also
> - **discover-plugins**: How marketplaces work · Official Anthropic marketplace (H3 Code intelligence, External integrations, Automatic security review, Development workflows, Output styles) · Community marketplace · Try it: add the demo marketplace · Add marketplaces (H3 Add from GitHub, other Git hosts, local paths, remote URLs) · Install plugins · Manage installed plugins (H3 Apply plugin changes without restarting) · Manage marketplaces (H3 Use the interactive interface, Use CLI commands, Configure auto-updates) · Configure team marketplaces · Security · Troubleshooting (H3 /plugin command not recognized, Common issues, Code intelligence issues) · Next steps

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **9 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_plugins_overview.md` | concept | plugins: intro, When to use plugins vs standalone configuration; plugins-reference: intro ("A plugin is…") | 500 | What a Claude Code plugin is (self-contained directory of skills/agents/hooks/MCP/LSP/monitors); the plugins-vs-standalone decision table; namespacing (`/plugin-name:skill`); when each is best. Links create→note 2, reference→notes 3-5. |
| 2 | `cc_plugin_quickstart.md` | procedure | plugins: Quickstart (Prerequisites, Create your first plugin steps), Develop a plugin in your skills directory, Convert existing configurations to plugins (Migration steps, What changes) | 650 | Steps to build a first plugin (dir, manifest, skill, `--plugin-dir` test, `$ARGUMENTS`); `claude plugin init` skills-dir dev (`@skills-dir`); migrate `.claude/` configs to a plugin; `/reload-plugins`. |
| 3 | `cc_plugin_directory_structure.md` | concept | plugins: Plugin structure overview; plugins-reference: Plugin directory structure (Standard plugin layout, File locations reference) | 450 | The plugin root layout (`.claude-plugin/`, `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `monitors/`, `bin/`, `settings.json`); component → default-location table; the "don't nest dirs in `.claude-plugin/`" rule; single-`SKILL.md`-at-root layout. |
| 4 | `cc_plugin_manifest_schema.md` | concept | plugins-reference: Plugin manifest schema (Complete schema, Required fields, Unrecognized fields, Metadata fields, Default enablement, Component path fields, Experimental components, Path behavior rules) | 700 | `.claude-plugin/plugin.json` schema: required `name`, metadata fields (`displayName`/`version`/`author`/`keywords`/`defaultEnabled`), component-path fields and replace-vs-extend behavior, unrecognized-field tolerance + `--strict`, experimental components. `dependencies`/`version-resolution` → B09B. |
| 5 | `cc_plugin_components.md` | concept | plugins-reference: Plugin components reference (Skills, Agents, Hooks, MCP servers, LSP servers, Monitors, Themes); plugins: Develop more complex plugins (Add Skills, Add LSP servers, Add background monitors, Ship default settings) | 750 | The seven component types a plugin can ship — skills, agents (supported frontmatter fields), hooks (event list + types), MCP servers, LSP servers, monitors, themes — with location/format per type and `settings.json` default-agent activation. Authoring detail → B06/B07/B08/B10. |
| 6 | `cc_plugin_user_config_and_env.md` | concept | plugins-reference: User configuration, Channels, Environment variables (+ Persistent data directory) | 600 | `userConfig` prompts (`type`/`title`/`sensitive`/etc.) and `${user_config.KEY}` substitution; `channels` declarations; the three path variables `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${CLAUDE_PROJECT_DIR}` and the persistent-data-dir pattern. |
| 7 | `cc_plugin_cli_commands.md` | procedure | plugins-reference: CLI commands reference (init/install/uninstall/prune/enable/disable/update/list/details/tag), Plugin installation scopes, Skills-directory plugins (Choose where it loads, Edit/reload/disable) | 700 | The `claude plugin` / `/plugin` CLI surface: init, install, uninstall (`--keep-data`), enable/disable, update, list, details (token cost), with the four install scopes (user/project/local/managed); skills-dir plugin load rules + trust. `prune`/`tag` dependency semantics → B09B. |
| 8 | `cc_plugin_marketplaces_and_install.md` | procedure | discover-plugins: How marketplaces work, Official/Community/demo marketplace, Add marketplaces (GitHub/Git/local/remote), Install plugins, Manage installed plugins (+reload), Manage marketplaces (interactive/CLI/auto-update), Configure team marketplaces, Security; plugins: Submit your plugin to the community marketplace | 750 | The discover→add-marketplace→install flow; the official/community/demo catalogs and how to add each; `/plugin install name@marketplace`; install scopes; manage/enable/disable/auto-update marketplaces; `extraKnownMarketplaces` team config; the trust/arbitrary-code security warning. Marketplace **creation** → B09B. |
| 9 | `cc_plugin_caching_and_troubleshooting.md` | procedure | plugins-reference: Plugin caching and file resolution (Path traversal, symlinks), Debugging and development tools (Debugging commands, Common issues, Example errors, Hook/MCP troubleshooting, Directory structure mistakes); discover-plugins: Troubleshooting (/plugin not recognized, Common issues, Code intelligence issues) | 700 | The plugin cache (`~/.claude/plugins/cache`), 7-day orphan grace, path-traversal limits and symlink rules; `claude --debug`; the common-issues / error-message tables; hook/MCP/structure debug checklists; `/plugin` command-recognition and code-intelligence fixes. Version management → note 8 / B09B. |

**Estimate: 9 notes** — concept ×5 (notes 1,3,4,5,6), procedure ×4 (notes 2,7,8,9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (14,190 words). New `cc_` notes: 9. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,800 (avg ~640/note). Code blocks: ≤6/note (source is code-dense — each note carries only the 2-5 verbatim examples essential to its concept; full schemas are summarized in tables, not pasted wholesale).
- **Building Block Distribution**: concept ×5 (notes 1,3,4,5,6) · procedure ×4 (notes 2,7,8,9). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> *Liskov Substitution Principle*, NOT Language Server Protocol, so it is **excluded** from the LSP context).

### 1. `cc_plugins_overview` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — A plugin is the packaging/sharing unit for Claude Code extensions; this note defines what extends, so the product term is its definitional anchor.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — The note's "self-contained directory of components that extends the host without recompiling it" IS the plugin-SDK / extensible-host pattern this term generalizes (VS Code / Obsidian / WordPress lineage).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — A plugin's identity (name, version, namespace) lives in its `.claude-plugin/plugin.json` manifest, the declaration the note introduces as defining the plugin.
- [Skills](../../term_dictionary/term_skills.md) — Skills are the headline component a plugin packages; the plugins-vs-standalone table compares `/hello` (standalone skill) against `/plugin-name:hello` (plugin-namespaced skill).
- [Subagent](../../term_dictionary/term_subagent.md) — Agents are one of the four component types a plugin bundles; the note lists subagents among what plugins share across projects and teams.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — MCP servers are a core plugin component the note names as part of "skills, agents, hooks, and MCP servers"; plugins bundle pre-configured MCP integrations.
- [Atomic Skill](../../term_dictionary/term_atomic_skill.md) — The note distinguishes single-project standalone customization from versioned, shareable plugin packaging; an atomic skill is the smallest such reusable unit a plugin distributes.

### 2. `cc_plugin_quickstart` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the hands-on procedure for building a plugin for Claude Code itself (`claude --plugin-dir`, `claude plugin init`), so the product term grounds every command.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — Step 2 of the quickstart creates `.claude-plugin/plugin.json` with name/description/version — the manifest this term defines, the file the host loader reads before activation.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — The quickstart's "Add a skill" step authors `skills/hello/SKILL.md` with YAML frontmatter + body — exactly the SKILL.md skill-manifest contract this term documents.
- [Skills](../../term_dictionary/term_skills.md) — The plugin built in this quickstart ships a single skill; the `$ARGUMENTS` placeholder and `/reload-plugins` steps are skill-authoring mechanics.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `claude plugin init` scaffolds the authoring surface (manifest + starter SKILL.md) that the plugin-SDK/extensible-host pattern exposes to third-party developers.
- [Claude](../../term_dictionary/term_claude.md) — The quickstart tests the plugin by invoking the skill and observing Claude respond; the model is what consumes the skill the plugin packages.

### 3. `cc_plugin_directory_structure` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents the on-disk layout Claude Code's loader scans to discover a plugin's components, so the product term grounds the directory contract.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — The `.claude-plugin/plugin.json` manifest is the one file allowed inside `.claude-plugin/`; the note's central rule ("only the manifest goes there") is about manifest placement.
- [Skills](../../term_dictionary/term_skills.md) — The `skills/<name>/SKILL.md` directory is the primary component layout the note specifies, plus the single-skill-at-root shortcut.
- [Subagent](../../term_dictionary/term_subagent.md) — The `agents/` directory holds subagent definitions, one of the standard plugin-root component folders the file-locations table enumerates.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `.mcp.json` at the plugin root is the standard location for MCP server definitions, a row in the note's component-location table.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — The default-locations-plus-optional-manifest discovery model the note describes is the plugin-SDK convention of a host auto-discovering components in well-known folders.

### 4. `cc_plugin_manifest_schema` (6 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — This note IS the field-by-field reference for `.claude-plugin/plugin.json` — the plugin manifest this term defines, including the version/compat declaration pattern it describes.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — The manifest's component-path fields (`skills`/`commands`/`agents`/`hooks`/`mcpServers`/`lspServers`) are the registration surface the plugin-SDK pattern exposes; replace-vs-extend rules govern how the host loads them.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The schema is consumed by Claude Code's plugin loader; `claude plugin validate --strict` and version v2.1.x gates are product behaviors the note documents.
- [Version Set](../../term_dictionary/term_version_set.md) — The `version` field pins update behavior (explicit semver vs commit-SHA fallback); a version set is the analogous build-pinning concept for grouping versioned artifacts.
- [Skills](../../term_dictionary/term_skills.md) — The `skills` manifest field *adds to* the default `skills/` dir while most fields replace — a path-behavior rule that hinges on how skills are discovered and namespaced.
- [Subagent](../../term_dictionary/term_subagent.md) — The `agents` field points at subagent files; `settings.json`'s `agent` key (referenced from the schema) activates a plugin subagent as the main thread.

### 5. `cc_plugin_components` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note enumerates every component type a Claude Code plugin can contribute; the product term defines the host these components extend.
- [Skills](../../term_dictionary/term_skills.md) — Skills (model-invoked `/name` shortcuts) are the first and most common component type; the note specifies their `skills/`/`commands/` location and discovery behavior.
- [Subagent](../../term_dictionary/term_subagent.md) — Agents are a component type with their own supported frontmatter (`model`/`effort`/`maxTurns`/`disallowedTools`/`isolation`); the note lists which fields are allowed and which (`hooks`/`mcpServers`/`permissionMode`) are blocked for security.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — MCP servers are a bundled component type (`.mcp.json`); the note shows their config and that plugin MCP servers start automatically when the plugin is enabled.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — LSP servers are configured via `.lsp.json` as a pluggable component; this is the same provider-plugin pattern (a typed config record the host loads to add a capability without core changes) that this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Every component type ultimately surfaces tools/capabilities Claude can invoke (MCP tools, hook actions, monitor notifications); the components are how a plugin grows the model's tool-use surface.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Plugin agents cannot ship `hooks`/`mcpServers`/`permissionMode`, and monitors run unsandboxed at hook trust level — security restrictions that reflect graduated-trust gating of what plugin code may do.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — The hooks component responds to ~30 lifecycle events (SessionStart, PreToolUse, SubagentStart, PreCompact, etc.); these are the agent-lifecycle events plugin hooks attach to.

### 6. `cc_plugin_user_config_and_env` (6 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `userConfig` and `channels` are top-level `plugin.json` fields; this note documents the parts of the manifest that drive enable-time prompting and path substitution.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — The `${user_config.KEY}` / `${CLAUDE_PLUGIN_ROOT}` substitution surface and `CLAUDE_PLUGIN_OPTION_<KEY>` exports are the plugin-SDK runtime contract between host and out-of-tree code.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The persistent-data-dir layout (`~/.claude/plugins/data/{id}/`) and update-mid-session path semantics are Claude Code host behaviors this note specifies.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note's variable substitutions apply to MCP server configs (command/args/env), and the `channels` field binds each channel to a plugin-provided MCP server.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — `${CLAUDE_PLUGIN_DATA}` is the persistent state directory that survives plugin updates (node_modules, caches, generated state) — the durable per-plugin memory store this note's pattern manages.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — Non-sensitive `userConfig` values can be substituted into skill and agent content; the note ties config substitution to the SKILL.md content the skill-manifest contract carries.

### 7. `cc_plugin_cli_commands` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the reference for the `claude plugin` / `/plugin` CLI surface, so the product term grounds every subcommand.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `claude plugin init` scaffolds a manifest; `claude plugin validate` checks it; `plugin details` reads its declared components — the CLI operates on the manifest this term defines.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `plugin init --with skills agents hooks mcp lsp` scaffolds the authoring surface the plugin-SDK pattern exposes; the CLI is the developer entry point to that surface.
- [Skills](../../term_dictionary/term_skills.md) — Skills-directory plugins (`@skills-dir`) load with no install step; `plugin init` writes to `~/.claude/skills/<name>/`, and `plugin details` groups `skills/`+`commands/` as Skills.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Project-scope `@skills-dir` plugins load only after the workspace trust dialog, and their MCP/LSP/monitor components are further restricted — the scope/trust gating this note documents.
- [Version Set](../../term_dictionary/term_version_set.md) — `plugin update`/`install` resolve a plugin's version (semver vs commit SHA) the way a version set pins a coordinated build; the CLI's update behavior keys off that version.
- [Subagent](../../term_dictionary/term_subagent.md) — `plugin details` reports the agents a plugin contributes and their token cost; `--scope` flags govern where subagent-bearing plugins install.

### 8. `cc_plugin_marketplaces_and_install` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the install/discover flow for Claude Code plugins (`/plugin`, `/plugin marketplace add`, install scopes), so the product term grounds the procedure.
- [Marketplace ID](../../term_dictionary/term_marketplace_id.md) — A plugin marketplace is a named catalog (`claude-plugins-official`, `claude-community`, `@marketplace-name`) referenced in `plugin install name@marketplace`; the marketplace identifier is the namespace the note's install commands key on.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — Installed plugins carry their `.claude-plugin/plugin.json` manifest; the **Will install** detail pane and component inventory the note describes read from it.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — Marketplaces distribute plugins authored against the plugin-SDK surface; the official catalogs (code-intelligence, external-integrations, dev-workflow plugins) are bundles of such extensions.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — The note's security warning (plugins/marketplaces execute arbitrary code; only add trusted sources) is the supply-chain trust concern this attack term concretizes for the install path.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Install scopes (user/project/local/managed) and the team-marketplace trust prompt are graduated-trust controls over who a plugin reaches and what it may do.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Many marketplace plugins (github, linear, notion, slack) bundle pre-configured MCP servers; the external-integrations catalog the note lists is MCP-server packaging.

### 9. `cc_plugin_caching_and_troubleshooting` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents Claude Code's plugin cache, `claude --debug`, and the `/plugin` Errors tab — host-specific caching and diagnostics behavior.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — The top failure modes the note triages are invalid/corrupt `plugin.json`, missing required `name`, and conflicting manifests — manifest-validation errors this term's gate is meant to catch.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — The cache copies marketplace plugins out of their source and blocks path-traversal/external symlinks for security — supply-chain isolation this attack term motivates.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — A full troubleshooting subsection covers plugin MCP servers not starting / tools not appearing, using `claude --debug` to read MCP initialization errors.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — The code-intelligence troubleshooting section (LSP server not starting, `Executable not found in $PATH`, high memory) is about the LSP-config provider-plugin pattern this term generalizes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Symlink resolution rules (preserve within-plugin, dereference within-marketplace, skip outside) and the cache-isolation model are trust-boundary controls the note enforces during caching.

## Section Coverage Map

```
plugins.md
├── intro ("Plugins let you extend…") ──────────── → note 1 (cc_plugins_overview)
├── When to use plugins vs standalone config ───── → note 1
├── Quickstart (Prerequisites, Create first plugin) → note 2 (cc_plugin_quickstart)
├── Develop a plugin in your skills directory ───── → note 2 (+ note 7 load rules)
├── Plugin structure overview ──────────────────── → note 3 (cc_plugin_directory_structure)
├── Develop more complex plugins
│   ├── Add Skills to your plugin ──────────────── → note 5 (cc_plugin_components) → B06
│   ├── Add LSP servers to your plugin ─────────── → note 5
│   ├── Add background monitors to your plugin ──── → note 5
│   ├── Ship default settings with your plugin ─── → note 5 (settings.json agent key)
│   ├── Organize complex plugins ───────────────── → note 3 (links plugins-reference structure)
│   ├── Test your plugins locally ──────────────── → note 2 (--plugin-dir / --plugin-url / reload)
│   ├── Debug plugin issues ────────────────────── → note 9 (cc_plugin_caching_and_troubleshooting)
│   ├── Share your plugins ─────────────────────── → linked out (B09B plugin-marketplaces; note 8 submit)
│   └── Submit your plugin to community marketplace → note 8 (cc_plugin_marketplaces_and_install)
├── Convert existing configurations to plugins
│   ├── Migration steps ────────────────────────── → note 2
│   └── What changes when migrating ────────────── → note 2
└── Next steps (For users / For developers) ─────── → notes 1/2/8 (links)
plugins-reference.md
├── intro ("A plugin is a self-contained dir…") ── → note 1
├── Plugin components reference
│   ├── Skills ─────────────────────────────────── → note 5 → B06
│   ├── Agents ─────────────────────────────────── → note 5 → B10A
│   ├── Hooks (event list + hook types) ────────── → note 5 → B07A
│   ├── MCP servers ────────────────────────────── → note 5 → B08A
│   ├── LSP servers (fields, available plugins) ── → note 5
│   ├── Monitors ───────────────────────────────── → note 5
│   └── Themes ─────────────────────────────────── → note 5
├── Plugin installation scopes ─────────────────── → note 7 (cc_plugin_cli_commands) → B03A
├── Skills-directory plugins (load rules, edit) ── → note 7
├── Plugin manifest schema
│   ├── Complete schema / Required fields ───────── → note 4 (cc_plugin_manifest_schema)
│   ├── Unrecognized fields / Metadata fields ──── → note 4
│   ├── Default enablement ─────────────────────── → note 4
│   ├── Component path fields / Path behavior ───── → note 4
│   ├── Experimental components ─────────────────── → note 4
│   ├── User configuration ─────────────────────── → note 6 (cc_plugin_user_config_and_env)
│   ├── Channels ───────────────────────────────── → note 6 (→ B08B channels)
│   └── Environment variables (+ persistent data) ─ → note 6
├── Plugin caching and file resolution
│   ├── Path traversal limitations ─────────────── → note 9
│   └── Share files with symlinks ──────────────── → note 9
├── Plugin directory structure (layout, locations) → note 3
├── CLI commands reference (init…tag) ──────────── → note 7 (prune/tag dependency semantics → B09B)
├── Debugging and development tools ────────────── → note 9
├── Distribution and versioning reference
│   └── Version management ──────────────────────── → note 8 (cc_plugin_marketplaces_and_install; → B09B plugin-dependencies)
└── See also (cards) ───────────────────────────── → notes 1/8 (links)
discover-plugins.md
├── intro ──────────────────────────────────────── → note 8
├── How marketplaces work ──────────────────────── → note 8
├── Official Anthropic marketplace
│   ├── Code intelligence (LSP catalog) ────────── → note 8 (catalog) / note 5 (create LSP) / note 9 (troubleshoot)
│   ├── External integrations (MCP plugins) ────── → note 8
│   ├── Automatic security review ──────────────── → note 8 (→ B16 security-guidance)
│   ├── Development workflows ───────────────────── → note 8
│   └── Output styles ──────────────────────────── → note 8 (→ B06 output-styles)
├── Community marketplace ──────────────────────── → note 8
├── Try it: add the demo marketplace ───────────── → note 8
├── Add marketplaces (GitHub/Git/local/remote) ── → note 8
├── Install plugins ────────────────────────────── → note 8 (scopes shared w/ note 7)
├── Manage installed plugins (+ reload) ────────── → note 8
├── Manage marketplaces (UI/CLI/auto-update) ───── → note 8
├── Configure team marketplaces ────────────────── → note 8 (extraKnownMarketplaces → B03A settings)
├── Security ───────────────────────────────────── → note 8 (→ B16)
├── Troubleshooting
│   ├── /plugin command not recognized ─────────── → note 9
│   ├── Common issues ──────────────────────────── → note 9
│   └── Code intelligence issues ───────────────── → note 9
└── Next steps ─────────────────────────────────── → notes 1/8 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| plugins (2.97Kw, 7 H2, concept+procedure mixed) | notes 1, 2, 3 + link-outs (note 5, 8, 9) | distinct BBs: what-a-plugin-is (concept) vs build-it (procedure) vs layout (concept); complex-component how-tos route to the reference notes |
| plugins-reference (8.26Kw >2500, 10 H2 / 41 H3) | notes 1, 3, 4, 5, 6, 7, 9 | far exceeds density cap; split by sub-concern — components ref / manifest schema / user-config+env / directory structure / CLI / caching+debugging — each BB-atomic |
| discover-plugins (2.96Kw, 12 H2, procedure+catalog) | note 8 + note 9 (troubleshooting) | install/marketplace procedure is one cohesive flow (note 8); its troubleshooting section joins the reference debugging note (note 9) for a single triage note |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_plugins_overview | concept | 500 | 1 | ✅ |
| 2 | cc_plugin_quickstart | procedure | 650 | 6 | ✅ |
| 3 | cc_plugin_directory_structure | concept | 450 | 2 | ✅ |
| 4 | cc_plugin_manifest_schema | concept | 700 | 3 | ✅ |
| 5 | cc_plugin_components | concept | 750 | 5 | ✅ |
| 6 | cc_plugin_user_config_and_env | concept | 600 | 4 | ✅ |
| 7 | cc_plugin_cli_commands | procedure | 700 | 5 | ✅ |
| 8 | cc_plugin_marketplaces_and_install | procedure | 750 | 6 | ✅ |
| 9 | cc_plugin_caching_and_troubleshooting | procedure | 700 | 3 | ✅ |

No note approaches the 2,500-word / 400-line caps; the source is code-dense, so notes 2/5/8 ride at exactly the ≤6-code-block cap and summarize remaining schemas in tables rather than pasting them. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_plugins_overview cc_plugin_quickstart cc_plugin_directory_structure cc_plugin_manifest_schema cc_plugin_components cc_plugin_user_config_and_env cc_plugin_cli_commands cc_plugin_marketplaces_and_install cc_plugin_caching_and_troubleshooting"
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

Single phase (9 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 9 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 9 notes receives ≥1 inbound link from a vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB confirms in-degree ≥1 for all 9 after inlinks applied | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 9 rows** under a "Plugins" cluster + increments the BB-distribution counts
(concept ×5, procedure ×4). The entry-point back-link is added to each note at finalization (G7/G8).

## Undigested Terms Plan (Step 2d)

B09A creates **0 new `term_dictionary` captures** — plugin vocabulary is covered by a B09A `cc_` concept/procedure
note, an existing substantive term note (link), or a sibling sub-plan (Pattern B; dedup checked across
`term_dictionary/` AND `resources/documentation/`):

| Term surfaced in pages | Disposition |
|---|---|
| Plugin | note 1 `cc_plugins_overview` (doc concept) + link `term_plugin_sdk` (exists) |
| Plugin manifest (`plugin.json`) | note 4 `cc_plugin_manifest_schema` + link `term_plugin_manifest` (exists) |
| SKILL.md / skill manifest | link `term_skill_manifest` (exists); detail → B06 `skills` |
| Marketplace | note 8 `cc_plugin_marketplaces_and_install` + link `term_marketplace_id` (exists); **creation → B09B** |
| LSP server / code intelligence | notes 5/8/9 (doc concept) — link `term_provider_plugin` (config-as-plugin analog). **NOTE: `term_lsp` = Liskov Substitution Principle, NOT Language Server Protocol → excluded.** No CC LSP term note exists; owned as doc concept (B09A/B03B), no new capture. |
| Background monitor | note 5 `cc_plugin_components` (doc concept) — tied to Monitor tool (B03B `tools-reference`) |
| Theme / output style | note 5 (mention) / output-styles → B06 |
| Hook / event | note 5 (component list) — semantics → B07A (`hooks`) |
| MCP server / channel | note 5/6 (component) — link `term_mcp` (exists); channels detail → B08B |
| Subagent / agent | note 5 (component) — link `term_subagent` (exists); config → B10A |
| Install scope (user/project/local/managed) | note 7 — detail → B03A `settings` |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${CLAUDE_PROJECT_DIR}` | note 6 (doc concept) |
| `userConfig` | note 6 (doc concept) |
| Plugin dependency / `dependencies` / version constraint | **owned by B09B** (`plugin-dependencies`) — linked, not captured |
| Semantic versioning / commit-SHA version | note 8 (version management) + link `term_version_set` (analog) |
| Plugin cache | note 9 (doc concept) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/captions/code-comments
for newly-surfaced non-glossary terms. Candidates checked against existing notes + sibling sub-plans:
`term_plugin_manifest`, `term_plugin_sdk`, `term_skill_manifest`, `term_provider_plugin`, `term_marketplace_id`,
`term_version_set`, `term_dependency_confusion`, `term_acp`, `term_json_rpc` all exist → linked. The one
genuinely-new concept with no doc-page home AND no existing note — **"Language Server Protocol (LSP) server"**
— is a documentation concept (not a glossary vocabulary term), digested as `cc_` doc content in notes 5/8/9 per
Pattern B (NOT a `term_dictionary` capture; `term_lsp` is the Liskov term, a false positive). **0 new B09A `term_dictionary` captures.**

## Term-Note Authoring Requirements

**N/A for B09A** — it authors zero term notes (all routed above to existing notes / sibling sub-plans). The full
template, MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim; one BB per note. Each note ≤400 lines (split if a draft >350). Cap fan-out at ~30 agents/run.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_plugin_sdk.md` | notes 1, 4 | plugin-SDK term → CC plugin definition + manifest schema |
| `term_dictionary/term_plugin_manifest.md` | notes 4, 3 | plugin-manifest term → CC manifest schema + directory structure |
| `term_dictionary/term_provider_plugin.md` | note 5 | provider-plugin term → CC plugin component types (LSP config-as-plugin) |
| `term_dictionary/term_marketplace_id.md` | note 8 | marketplace term → CC plugin marketplace/install flow |
| `term_dictionary/term_claude_code.md` | notes 1, 7 | CC product term → plugin overview + CLI surface |
| `documentation/tutorials/tutorial_claude_code_02_aim_plugins.md` | note 2 | AIM plugin tutorial → CC plugin quickstart |

## Follow-up Recommendations

- After the 9 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 9 rows for `entry_claude_code_docs.md` under a "Plugins" cluster; `/tessellum-check-broken-links`; verify DB in-degree ≥1 for all 9 (G7/G8).
- Coordinate sibling cross-links with B09B (marketplaces/dependencies) once both execute — notes 4/7/8 forward-reference B09B sections (`plugin-marketplaces`, `plugin-dependencies`); add reciprocal links post-execution.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE (skeleton) |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-13** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B09A, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read fully from `inbox/claude_code_docs/`; measured words match the master (plugins 2,973 · plugins-reference 8,257 · discover-plugins 2,960 = 14,190). Measured structure: plugins 7 H2 / 15 H3 / 10 code; plugins-reference 10 H2 / 41 H3 / 33 code; discover-plugins 12 H2 / 16 H3 / 22 code. The 8.26Kw reference page far exceeds the 2,500-word cap → split into 7 notes (components / manifest schema / user-config+env / directory structure / CLI / caching+debugging, plus the shared definition into note 1).
- **Notes**: 9 (concept 5, procedure 4) — within master estimate. Splits documented in Split Decisions.
- **Critical false-positive caught**: `term_lsp` resolves to the *Liskov Substitution Principle* (SOLID), NOT Language Server Protocol — **excluded** from the LSP/code-intelligence context; LSP-server is digested as a `cc_` doc concept and the analogous existing term `term_provider_plugin` is linked instead.
- **Step 2d new-term scan**: 1 genuine new concept surfaced ("Language Server Protocol server") → owned as doc concept (B09A/B03B), **0 new B09A term captures**. All other surfaced terms map to existing term notes or sibling sub-plans.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G7/G8 gate rows, Inlinks table, Undigested Terms Plan with B09B ownership boundary.
- **28-item checklist**: PASS (term-note authoring items N/A — B09A authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and reviewed; set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B09A contributes 9 rows under a "Plugins" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 9 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | All 9 notes 450–750w. Notes 2/5/8 ride the ≤6-code-block cap; remaining schemas summarized in tables, not pasted — verified within caps. The 8.26Kw reference page is split into 7 notes, no note >750w. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Spot-check: plugins-reference measured 8,257 = plan 8,257; plugins 2,973 = plan 2,973; discover-plugins 2,960 = plan 2,960. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B09A authors 0 term notes; Undigested Terms Plan routes every plugin term to an existing note / sibling sub-plan / doc concept; Authoring Requirements inherited. |
| CP9 | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs). Collision check performed: `term_plugin_manifest`, `term_plugin_sdk`, `term_skill_manifest`, `term_provider_plugin`, `term_marketplace_id`, `term_version_set` all exist → linked, not recreated. `term_lsp` collision (Liskov vs LSP) explicitly resolved by exclusion. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.

**Source**: https://code.claude.com/docs/en/plugins
**Last Updated**: 2026-06-13
**Status**: Active
