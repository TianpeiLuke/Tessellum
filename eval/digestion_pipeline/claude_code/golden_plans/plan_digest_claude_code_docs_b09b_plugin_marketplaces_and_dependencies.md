---
title: Sub-Plan B09B — Claude Code Docs: Plugin Marketplaces & Dependencies
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["plugin-marketplaces", "plugin-dependencies", "plugin-hints"]
---

# Sub-Plan B09B: Plugin Marketplaces & Dependencies

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 plugin-distribution pages that cover how plugins are catalogued, hosted, version-pinned, and
recommended: building and hosting a `marketplace.json` catalog, the marketplace/plugin source-type schema,
managed-settings restrictions on which marketplaces are allowed, plugin-to-plugin dependency version
constraints (semver + git-tag resolution), and the `<claude-code-hint />` CLI install-prompt protocol.
P2 (Phase B) — builds on the plugin core defined in B09A (`plugins.md`, `plugins-reference.md`,
`discover-plugins.md`), which owns the plugin-creation and install-from-marketplace material; B09B owns
the **distribution** half (authoring/hosting marketplaces and dependency management).

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 9,840 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the `marketplace.json` schema + plugin source types (the load-bearing distribution
  reference) and the dependency-constraint/semver/git-tag model (the most novel, reference-dense topic).
- **Group**: split `plugin-marketplaces` (6.4Kw, far over the 2,500-word cap) into 4 BB-atomic notes —
  authoring walkthrough (procedure) vs schema reference (concept) vs hosting+managed-settings (procedure)
  vs CLI subcommands + troubleshooting (procedure). Keep `plugin-dependencies` as 1 concept note + 1
  procedure note (declare/resolve vs tag/prune CLI ops). Keep `plugin-hints` as 1 self-contained
  procedure note.
- **Skip / link-out (own other sub-plans)**: creating plugins / plugin component layout / installing from
  a marketplace → B09A (`plugins.md`, `discover-plugins.md`); `plugins-reference` caching, `${CLAUDE_PLUGIN_ROOT}`,
  `${CLAUDE_PLUGIN_DATA}`, installation scopes, default-enablement → B09A; `extraKnownMarketplaces` /
  `strictKnownMarketplaces` / `enabledPlugins` full settings reference → B03A (`settings.md`); `env-vars`
  full reference (`GITHUB_TOKEN`, `CLAUDE_CODE_PLUGIN_*`, `CLAUDECODE`) → B03A (`env-vars.md`); hooks /
  MCP / LSP component semantics → B07A/B08A/B03B; GHES marketplace restrictions → B13B
  (`github-enterprise-server.md`). These are referenced via links, never duplicated.

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| plugin-marketplaces | /plugin-marketplaces | 6,410 | 36 | 9 | 18 | procedure/concept |
| plugin-dependencies | /plugin-dependencies | 2,189 | 6 | 7 | 0 | concept |
| plugin-hints | /plugin-hints | 1,241 | 6 | 6 | 0 | procedure |

> **H2 lists (document order):**
> - **plugin-marketplaces**: Overview · Walkthrough: create a local marketplace · Create the marketplace file · Marketplace schema (H3 Required fields, Owner fields, Optional fields) · Plugin entries (H3 Required fields, Optional plugin fields) · Plugin sources (H3 Relative paths, GitHub repositories, Git repositories, Git subdirectories, npm packages, Advanced plugin entries, Strict mode) · Host and distribute marketplaces (H3 Host on GitHub, Host on other git services, Private repositories, Test locally, Require marketplaces for your team, Pre-populate plugins for containers, Managed marketplace restrictions, Version resolution and release channels) · Validation and testing · Manage marketplaces from the CLI (H3 add, list, remove, update) · Troubleshooting (H3 ×7)
> - **plugin-dependencies**: Why constrain dependency versions · Declare a dependency with a version constraint · Depend on a plugin from another marketplace · Tag plugin releases for version resolution · How constraints interact · Enable or disable a plugin with dependencies · Remove orphaned auto-installed dependencies · Resolve dependency errors
> - **plugin-hints**: How it works · Emit the hint · Choose where to emit · What the user sees · Hint format · Requirements · Get your plugin into the official marketplace

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **7 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_plugin_marketplace_walkthrough.md` | procedure | plugin-marketplaces: Overview, Walkthrough (Steps), Validation and testing | 550 | End-to-end: create dir structure → SKILL.md → `plugin.json` → `marketplace.json` → add+install+run; `/plugin validate`. Links create-plugins (B09A), schema (note 2). |
| 2 | `cc_marketplace_json_schema.md` | concept | plugin-marketplaces: Create the marketplace file, Marketplace schema (req/owner/optional), Plugin entries (req/optional) | 650 | `marketplace.json` field reference: name/owner/plugins, reserved names, `metadata.pluginRoot`, `allowCrossMarketplaceDependenciesOn`; plugin-entry standard + component fields; `strict` mode. |
| 3 | `cc_plugin_sources.md` | concept | plugin-marketplaces: Plugin sources (relative/github/url/git-subdir/npm), Advanced entries, marketplace-vs-plugin-source note | 550 | The 5 source types + fields (`ref`/`sha`/`path`/`package`/`registry`); ref-vs-sha pinning; marketplace-source vs plugin-source distinction; `${CLAUDE_PLUGIN_ROOT}`→link B09A. |
| 4 | `cc_host_and_manage_marketplaces.md` | procedure | plugin-marketplaces: Host and distribute (GitHub/other/private/team/seed/version-channels), Manage from the CLI (add/list/remove/update), Troubleshooting | 700 | Host on GitHub/GitLab, private-repo auth tokens, `extraKnownMarketplaces`/`enabledPlugins`, seed dir, version resolution + release channels; `claude plugin marketplace` subcommands; troubleshooting table. |
| 5 | `cc_marketplace_restrictions.md` | procedure | plugin-marketplaces: Managed marketplace restrictions (strictKnownMarketplaces) | 450 | `strictKnownMarketplaces` allowlist (undefined/`[]`/list), exact vs `hostPattern`/`pathPattern` matching, enforcement timing, pairing with `extraKnownMarketplaces`; full ref→B03A settings. |
| 6 | `cc_plugin_dependencies.md` | concept | plugin-dependencies: all 8 H2 | 750 | Why constrain; `dependencies` array (name/version/marketplace); cross-marketplace allowlist; `{plugin}--v{ver}` git-tag resolution + `claude plugin tag`; constraint intersection; enable/disable cascade; `claude plugin prune`; error table. |
| 7 | `cc_plugin_install_hints.md` | procedure | plugin-hints: all 7 H2 | 500 | `<claude-code-hint />` marker protocol: `CLAUDECODE`/`CLAUDE_CODE_CHILD_SESSION` gating, emit to stderr, checks Claude Code runs, hint format/attributes, requirements (own-line + official marketplace), prompt UX. |

**Estimate: 7 notes** — concept ×3 (notes 2, 3, 6), procedure ×4 (notes 1, 4, 5, 7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (9,840 words). New `cc_` notes: 7. New `term_dictionary` notes: 0 (Pattern B — see Undigested Terms Plan).
- Est. total digest words: ~4,150 (avg ~593/note). Code blocks: ~3–6 per note (JSON manifests, shell commands) — all under the ≤6 cap.
- **Building Block Distribution**: concept ×3 (notes 2, 3, 6) · procedure ×4 (notes 1, 4, 5, 7). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_plugin_marketplace_walkthrough` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding CLI; relevance: the host tool whose `/plugin marketplace add` and `/plugin install` commands drive this entire walkthrough.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the `plugin.json`/manifest file declaring a plugin's identity and components; relevance: Step 3 of the walkthrough authors exactly this `plugin.json` (name/description/version) as the plugin's manifest.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — what-it-is: the `SKILL.md` frontmatter that defines a skill; relevance: Step 2 creates the `quality-review` `SKILL.md` whose frontmatter (`description`, `disable-model-invocation`) is the skill manifest.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged repeatable Claude Code workflows invocable via `/<name>`; relevance: the walkthrough's sample plugin bundles one skill, and the installed plugin is run as a namespaced skill `/quality-review-plugin:quality-review`.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — what-it-is: the contract/API a plugin package implements against its host; relevance: the directory + manifest layout the walkthrough builds is the plugin-package contract that a plugin SDK formalizes.
- [Claude Code MCP](../../term_dictionary/term_mcp.md) — what-it-is: Model Context Protocol for connecting external tools/data; relevance: the walkthrough notes plugins can bundle MCP servers alongside skills/agents/hooks, so MCP is one component a marketplace plugin can distribute.

### 2. `cc_marketplace_json_schema` (6 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the schema describing a plugin's metadata and component declarations; relevance: each `plugins[]` entry in `marketplace.json` accepts every plugin-manifest field plus marketplace-specific ones, so the manifest schema is the base this note extends.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding host; relevance: this `marketplace.json` schema is read and validated by Claude Code at marketplace-add time, defining what the tool ingests.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged workflows; relevance: `skills` is one of the component-configuration fields a plugin entry can declare custom paths for.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a Claude Code agent spawned with isolated context; relevance: `agents` is a plugin-entry component field giving custom paths to agent (subagent) definition files.
- [Claude Code MCP](../../term_dictionary/term_mcp.md) — what-it-is: Model Context Protocol; relevance: `mcpServers` is a plugin-entry component field carrying MCP server configs or a path to MCP config.
- [LSP (Language Server Protocol)](../../term_dictionary/term_language_server_protocol.md) — what-it-is: the IDE/code-intelligence protocol for language servers; relevance: `lspServers` is a plugin-entry component field declaring LSP server configurations a plugin can ship.

### 3. `cc_plugin_sources` (6 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the per-plugin manifest; relevance: each plugin source resolves a remote/local location into a plugin directory whose manifest Claude Code then loads, so sources are how the manifest is fetched.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager + registry with `package.json`/version ranges; relevance: the `npm` source type installs plugins via `npm install` with `package`/`version`/`registry` fields and semver ranges drawn directly from npm.
- [Version Set](../../term_dictionary/term_version_set.md) — what-it-is: Brazil's pinned set of dependency versions; relevance: `ref`/`sha` pinning on git sources fixes a plugin to an exact reproducible commit, the same pin-the-version concept a version set provides for builds.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — what-it-is: the plugin package contract; relevance: regardless of source type, what is fetched must satisfy the plugin package contract a plugin SDK defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the host that clones/copies the source into `~/.claude/plugins/cache`; relevance: Claude Code is the resolver that turns each source descriptor into a cached, version-keyed plugin install.

### 4. `cc_host_and_manage_marketplaces` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding host with `claude plugin marketplace` subcommands; relevance: this note documents Claude Code's own CLI for adding/listing/removing/updating marketplaces and its startup auto-update behavior.
- [CodeArtifact](../../term_dictionary/term_codeartifact.md) — what-it-is: AWS's private package/artifact repository; relevance: the private-registry and pre-populated-seed-directory hosting patterns (internal package distribution with auth tokens) parallel CodeArtifact's private artifact distribution.
- [Version Set](../../term_dictionary/term_version_set.md) — what-it-is: a pinned, reproducible version selection; relevance: the version-resolution-and-release-channels section pins plugins via `version`/SHA and assigns stable vs latest channels to user groups, the channeled-pinning idea a version set embodies.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the `plugin.json` manifest; relevance: version resolution reads `version` from the plugin's manifest first (over the marketplace entry, then the git SHA), so the manifest drives update detection here.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a packaged Claude Code agent; relevance: `enabledPlugins` and seed directories pre-enable plugins that ship subagents/skills/hooks, so the hosting config governs which packaged agents a team gets by default.

### 5. `cc_marketplace_restrictions` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the host enforcing the policy; relevance: Claude Code checks the allowlist before any network/filesystem op on marketplace add, install, update, refresh, and auto-update, and reads `strictKnownMarketplaces` from managed settings that users cannot override.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: Claude Code's tiered permission/trust model; relevance: restricting which plugin sources can be added is a supply-chain trust control, an organizational tier of the same graduated-trust posture that governs what code runs.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — what-it-is: the plugin package contract; relevance: marketplace restrictions gate which third-party plugin packages (and thus which plugin-SDK-conforming code) an organization permits to load.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — what-it-is: a supply-chain attack pulling a malicious package over the intended internal one; relevance: source allowlisting and reserved/blocked marketplace names defend against the same impersonation/supply-chain threat dependency confusion exploits.
- [CodeArtifact](../../term_dictionary/term_codeartifact.md) — what-it-is: AWS's private, access-controlled package repository; relevance: locking plugin sources to an approved internal allowlist mirrors how an org restricts package pulls to a controlled private artifact repository like CodeArtifact.

### 6. `cc_plugin_dependencies` (7 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the `plugin.json` manifest; relevance: dependencies are declared in the manifest's `dependencies` array (bare name or `{name, version, marketplace}` object), so the manifest schema is where this whole feature lives.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the package manager whose `semver` package defines range syntax; relevance: the `version` field accepts any Node `semver` range (`~2.1.0`, `^2.0`, `>=1.4`, hyphen/comparator), and `npm` sources interact specially with constraint checking.
- [Version Set](../../term_dictionary/term_version_set.md) — what-it-is: a pinned, intersected set of compatible dependency versions; relevance: when multiple plugins constrain one dependency, Claude Code intersects their ranges to one resolved version — the consistent-version-set resolution this term names.
- [Acyclic Dependencies Principle (ADP)](../../term_dictionary/term_adp_acyclic_dependencies_principle.md) — what-it-is: the principle that a dependency graph must be a DAG with no cycles; relevance: plugin dependencies form a resolved graph (enable cascades to dependencies, disable is blocked by dependents), governed by the acyclic-dependency-graph discipline ADP formalizes.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — what-it-is: a supply-chain attack via cross-source dependency resolution; relevance: cross-marketplace dependencies are blocked by default and gated by `allowCrossMarketplaceDependenciesOn` precisely to prevent silently pulling a plugin from an unreviewed source.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the resolver host; relevance: Claude Code auto-installs, intersects ranges, surfaces `range-conflict`/`no-matching-tag` errors in `/doctor` and `claude plugin list --json`, and prunes orphans — the engine this note documents.

### 7. `cc_plugin_install_hints` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the host that scans command output for hint markers and shows the install prompt; relevance: the entire `<claude-code-hint />` protocol is a Claude-Code-specific mechanism — it sets `CLAUDECODE`, strips the marker, and gates installs to official marketplaces.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — what-it-is: the per-plugin manifest; relevance: a hint's `value="name@marketplace"` targets a plugin (with its manifest) in the official Anthropic marketplace that the prompt offers to install.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — what-it-is: the plugin/CLI integration contract; relevance: this page is for CLI/SDK maintainers wiring their tool to recommend its companion plugin — the integration-author audience a plugin SDK serves.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: the model→tool invocation mechanism returning output to the loop; relevance: hints ride on Bash/PowerShell tool-call output, and Claude Code strips them before the output re-enters the model's tool-use loop so they cost no tokens.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged Claude Code workflows; relevance: the plugin a hint recommends typically bundles skills/agents/hooks, so accepting the hint installs a skill-bearing plugin to user scope.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: the user-confirmation/trust model; relevance: Claude Code never auto-installs from a hint — the user always confirms via a bounded once-per-plugin/once-per-session prompt, the consent gate graduated trust enforces.

## Section Coverage Map

```
plugin-marketplaces.md
├── Overview ──────────────────────────────── → note 1 (cc_plugin_marketplace_walkthrough)
├── Walkthrough: create a local marketplace ─ → note 1
│   └── (6 Steps: dir/skill/plugin.json/marketplace.json/install/run) → note 1
├── Create the marketplace file ───────────── → note 2 (cc_marketplace_json_schema)
├── Marketplace schema ────────────────────── → note 2
│   ├── Required fields / Owner fields ─────── → note 2
│   └── Optional fields (pluginRoot, allowCross…) → note 2
├── Plugin entries ────────────────────────── → note 2
│   ├── Required fields ────────────────────── → note 2
│   └── Optional plugin fields (std + component) → note 2 (defaultEnabled detail → link B09A)
├── Plugin sources ────────────────────────── → note 3 (cc_plugin_sources)
│   ├── Relative/GitHub/Git/git-subdir/npm ─── → note 3
│   ├── Advanced plugin entries ────────────── → note 3 (${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PLUGIN_DATA} → link B09A)
│   └── Strict mode ────────────────────────── → note 2 (strict field; xref note 3)
├── Host and distribute marketplaces ──────── → note 4 (cc_host_and_manage_marketplaces)
│   ├── GitHub/other git/private repos ─────── → note 4
│   ├── Test locally / Require for team ─────── → note 4 (extraKnownMarketplaces/enabledPlugins → link B03A settings)
│   ├── Pre-populate plugins for containers ── → note 4
│   ├── Managed marketplace restrictions ───── → note 5 (cc_marketplace_restrictions)
│   └── Version resolution and release channels → note 4 (Pin dependency versions → link note 6)
├── Validation and testing ────────────────── → note 1
├── Manage marketplaces from the CLI ──────── → note 4
│   └── add / list / remove / update ───────── → note 4
└── Troubleshooting (×7) ──────────────────── → note 4 (relative-path-in-URL + git-timeout + offline + auth)
plugin-dependencies.md
├── Why constrain dependency versions ─────── → note 6 (cc_plugin_dependencies)
├── Declare a dependency with a constraint ── → note 6
├── Depend on a plugin from another mkt ───── → note 6
├── Tag plugin releases for version res. ──── → note 6
├── How constraints interact ──────────────── → note 6
├── Enable or disable a plugin w/ deps ────── → note 6 (defaultEnabled → link B09A)
├── Remove orphaned auto-installed deps ───── → note 6
└── Resolve dependency errors ─────────────── → note 6
plugin-hints.md
├── How it works ──────────────────────────── → note 7 (cc_plugin_install_hints)
├── Emit the hint ─────────────────────────── → note 7 (CLAUDECODE/CLAUDE_CODE_CHILD_SESSION → link B03A env-vars)
├── Choose where to emit ──────────────────── → note 7
├── What the user sees ─────────────────────── → note 7
├── Hint format ───────────────────────────── → note 7
├── Requirements ──────────────────────────── → note 7
└── Get your plugin into the official mkt ─── → note 7
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| plugin-marketplaces (6,410w >2,500, 36 code blocks >6, 9 H2) | notes 1,2,3,4,5 | massively over every density cap; distinct BBs — walkthrough/CLI ops (procedure) vs schema + source-type reference (concept) vs hosting/managing (procedure) vs managed-settings restrictions (procedure). Each note stays ≤6 code blocks. |
| plugin-marketplaces: Managed marketplace restrictions | note 5 (own note) | `strictKnownMarketplaces` is an admin/policy procedure with its own allowlist matching rules + JSON examples; keeping it with hosting (note 4) would push note 4 past the code-block cap and mix audiences (author vs org-admin). |
| plugin-dependencies (2,189w, single coherent feature) | note 6 (kept whole) | under the word cap; one cohesive concept (dependency constraints + resolution). The CLI ops (`tag`/`prune`) are folded in as part of the same feature, not split out. |
| plugin-hints (1,241w) | note 7 (kept whole) | small, single self-contained procedure; no split needed. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_plugin_marketplace_walkthrough | procedure | 550 | 6 | ✅ (=6 cap) |
| 2 | cc_marketplace_json_schema | concept | 650 | 3 | ✅ |
| 3 | cc_plugin_sources | concept | 550 | 5 | ✅ |
| 4 | cc_host_and_manage_marketplaces | procedure | 700 | 6 | ✅ (=6 cap) |
| 5 | cc_marketplace_restrictions | procedure | 450 | 4 | ✅ |
| 6 | cc_plugin_dependencies | concept | 750 | 3 | ✅ |
| 7 | cc_plugin_install_hints | procedure | 500 | 2 | ✅ |

No note exceeds the caps (≤400 lines, ≤2,500 words, ≤6 code blocks). Notes 1 and 4 sit exactly at the
6-code-block cap — execution must select the most load-bearing JSON/shell blocks and prose-summarize the
rest; if a draft would exceed 6, move the overflow example into the adjacent concept note (2 or 3) or
prose-describe it. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_plugin_marketplace_walkthrough cc_marketplace_json_schema cc_plugin_sources cc_host_and_manage_marketplaces cc_marketplace_restrictions cc_plugin_dependencies cc_plugin_install_hints"
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

Single phase (7 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (verbatim JSON/shell) | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 7 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability (inbound) | each of the 7 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 at finalization |
| G8-Discoverability (entry) | each note linked from `entry_claude_code_docs.md` (rows contributed at execution) | entry-point row present + DB |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 7 rows** under a
"Plugins" cluster (alongside B09A) + increments the BB-distribution counts (concept +3, procedure +4).

## Undigested Terms Plan (Step 4e)

b09b creates **0 new `term_dictionary` captures**. Step 2d re-scan (2026-06-13) re-read all 3 pages,
scanning emphasis/tables/JSON keys/captions for newly-surfaced vocabulary. Every term is covered by a b09b
`cc_` doc-concept note (Pattern B — CC vocabulary terms are subjects of doc pages, digested as `cc_*`
notes by their home sub-plan, never inlined as term notes), an existing substantive term note (link), or
its home sub-plan:

| Term surfaced | Disposition | Dedup verdict |
|---|---|---|
| Plugin marketplace / `marketplace.json` | notes 1–5 `cc_*` (doc concept, B09B owns) | new doc concept; not a term note |
| Plugin source (relative/github/url/git-subdir/npm) | note 3 `cc_plugin_sources` (doc concept) | new doc concept |
| `strict` mode | note 2 (folded) | doc detail, not a standalone term |
| `strictKnownMarketplaces` / managed restrictions | note 5 `cc_marketplace_restrictions`; full settings ref → B03A | doc concept; settings field owned by B03A |
| Plugin dependency / version constraint / semver range | note 6 `cc_plugin_dependencies` (doc concept) | new doc concept |
| `{plugin-name}--v{version}` git-tag convention | note 6 (folded) | doc detail |
| `<claude-code-hint />` install-prompt protocol | note 7 `cc_plugin_install_hints` (doc concept) | new doc concept |
| Plugin manifest / `plugin.json` | link `term_plugin_manifest` (exists) | substantive note exists → link |
| Plugin (general concept) / Plugin SDK | link `term_plugin_sdk`; plugin core → B09A | exists → link |
| Skill / SKILL.md | link `term_skills` / `term_skill_manifest` (exist) | exist → link |
| MCP server / Subagent / agent | link `term_mcp` / `term_subagent` (exist) | exist → link |
| LSP server | link `term_language_server_protocol` (exists; NB `term_lsp` is Liskov Substitution — do NOT use) | exists → link |
| npm / semver / git tag / version pinning | link `term_npm` / `term_version_set` (exist) | exist → link |
| `CLAUDECODE` / `CLAUDE_CODE_CHILD_SESSION` / `GITHUB_TOKEN` / `CLAUDE_CODE_PLUGIN_*` env vars | full ref → B03A (`env-vars.md`) | owned by B03A; not B09B |

> **`term_managed_settings` DB-verify:** `ls .../term_dictionary/term_managed_settings.md` returned MISSING,
> so it is a **ghost** and is NOT linked anywhere in this plan. Note 5's locked 6 terms are
> *concept* is carried by prose + a link-out to B03A (`settings.md`), not a term link. Likewise `term_lsp`
> exists but is **Liskov Substitution Principle** (wrong sense) — `term_language_server_protocol` is used

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B09B authors zero term notes, so there are
no new slugs to audit. The collision check that matters (do the plugin-distribution concepts duplicate
existing notes?) was performed: `term_plugin_manifest`, `term_plugin_sdk`, `term_skill_manifest`,
`term_skills`, `term_mcp`, `term_subagent`, `term_npm`, `term_version_set`, `term_language_server_protocol`,
`term_claude_code` all exist → linked, not recreated. No `cc_` doc note duplicates an existing term note
(verified the `claude_code/` folder is empty and no existing term covers `marketplace.json`/plugin-source/
dependency-constraint at the same sense).

## Term-Note Authoring Requirements

**N/A for b09b** — it authors zero term notes (all routed above to existing term links or `cc_` doc
cross-domain Related Terms, glossary template, MathJax) are inherited from the master and apply to
sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (JSON manifests + shell commands must match the source byte-for-byte). One BB per
  note. Each note ≤400 lines / ≤6 code blocks (split or move overflow if a draft exceeds either).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase
  (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_plugin_manifest.md` | notes 2, 6 | manifest term → `marketplace.json` schema (entries extend the manifest) + `dependencies` array |
| `term_dictionary/term_plugin_sdk.md` | notes 1, 3 | plugin-package-contract term → walkthrough that builds it + source types that fetch it |
| `term_dictionary/term_version_set.md` | notes 3, 6 | version-pinning term → `ref`/`sha` source pinning + dependency semver resolution |
| `term_dictionary/term_npm.md` | notes 3, 6 | npm/semver term → npm plugin source + semver dependency ranges |
| `term_dictionary/term_claude_code.md` | notes 4, 7 | CC tool term → `claude plugin marketplace` CLI + the `<claude-code-hint />` protocol |

## Follow-up Recommendations

- After the 7 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify
  DB in-degree ≥1 for each note — G7); queue the 7 rows for `entry_claude_code_docs.md` under the Plugins
  cluster (G8); add sibling cross-links to/from the B09A plugin-core notes once both sub-plans execute;
  `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B09B, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read fully from `inbox/claude_code_docs/`; measured words
  match the master's figure (plugin-marketplaces 6,410 · plugin-dependencies 2,189 · plugin-hints 1,241 =
  9,840). plugin-marketplaces is 2.5× the word cap and 6× the code-block cap → forced into 5 notes; the
  master's 7-note estimate holds (5 + 1 + 1).
- **Notes**: 7 (concept 3, procedure 4) — exactly the master estimate. Splits documented in Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–7 term notes per note (15 distinct `term_dictionary/` terms), each with a what-it-is + per-link
  ghosts/wrong-sense during verification and excluded — note 5 was re-locked without `term_managed_settings`
  (the managed-settings *concept* is carried by prose + a B03A link-out), and `term_language_server_protocol`
  is used instead of `term_lsp`.
- **Dedup-before-create (G-B)**: searched both `term_dictionary/` and `documentation/` via bm25 + dense;
  `claude_code/` folder confirmed empty (B09B is the first plugins-distribution sub-plan to execute in
  Phase B); no `cc_` doc note duplicates an existing term note.
- **Step 2d new-term scan**: every surfaced term routed (table above) → **0 new B09B term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), Split Decisions, Density Re-Assessment, G5 verification note, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B09B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` (9/9 review checkpoints pass below).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 notes → CREATE required); B09B contributes 7 rows under Plugins cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 7 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body `## Overview`/`## Related Notes`/footer convention inherited verbatim from master Format Definition; matches existing `documentation/` notes. |
| CP6 | Borderline density → split | ✅ PASS | plugin-marketplaces (6,410w/36 code) split into 5; notes 1 & 4 flagged at the 6-code cap with overflow rule. All 7 notes ≤750w, ≤6 code. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` re-measured: plugin-marketplaces 6,410 = plan 6,410; plugin-dependencies 2,189 = plan 2,189; plugin-hints 1,241 = plan 1,241. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B09B authors 0 term notes; Undigested Terms Plan routes every surfaced term (table); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (10 existing terms linked not recreated; empty `claude_code/` folder; no `cc_` note duplicates a term). Ghost terms `term_managed_settings`/`term_lsp`(wrong-sense) caught and excluded. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
