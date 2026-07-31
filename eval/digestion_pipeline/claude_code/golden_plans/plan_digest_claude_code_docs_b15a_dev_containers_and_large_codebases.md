---
title: Sub-Plan B15A — Claude Code Docs: Dev Containers & Large Codebases
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["devcontainer", "large-codebases"]
---

# Sub-Plan B15A: Dev Containers & Large Codebases

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The two operational/enterprise pages that cover running Claude Code in an isolated, reproducible
**development container** and configuring it for a **monorepo or large single-tree codebase** so it stays
focused on the code a task touches. P3 (Phase C) — specialized rollout guidance that builds on the P1
cores (memory, permissions, settings, skills, subagents, MCP, worktrees, sandboxing) those earlier
sub-plans define; this references that vocabulary via links, never re-digesting it. No glossary page in
this sub-plan; new non-glossary terms are routed per Pattern B (see Undigested Terms Plan).

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 6,376 measured words. **Planned: 6 notes.**

## Content Strategy

- **Prioritize**: the concrete, committed-vs-local configuration mechanics (dev-container feature, named
  volume mounts, managed settings, egress firewall; nested CLAUDE.md, `claudeMdExcludes`, `Read` deny
  rules, `worktree.sparsePaths`, `additionalDirectories`/`--add-dir`, per-directory skills) — these are
  the operational payload teammates copy.
- **Group**: split `devcontainer` into a setup procedure (install + reference container) vs a hardening
  procedure (persist/policy/egress/no-prompts); split `large-codebases` (16 code blocks) by mechanism
  family — strategy/where-to-start, CLAUDE.md layering, read-reduction + worktree scoping, skills +
  plugins — so each note stays under the ≤6-code-block cap.
- **Skip / link-out (own other sub-plans)**: sandbox comparison → B05B (`sandbox-environments`); managed
  settings keys + settings hierarchy → B03A / B14B (`server-managed-settings`); permission modes / auto
  mode / `--dangerously-skip-permissions` → B05A; env-vars reference → B03A; MCP → B08A; memory/CLAUDE.md
  loading internals → B02B; worktree settings reference → B10B/B03A; skills/plugins reference → B06/B09;
  hooks → B07A/B07B; cost/monitoring → B02A/B15B; cloud provider credentials → B14A; admin rollout →
  B14B. These are referenced via links, never duplicated.
- **Terms**: no glossary page here; the few capitalized concepts (dev container, sparse checkout, code
  intelligence/LSP, managed settings) route to existing term notes or their home sub-plan (Pattern B; see
  Undigested Terms Plan) — no inline term definitions.

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| devcontainer | /devcontainer | 2,091 | 3 | 6 | 0 | procedure |
| large-codebases | /large-codebases | 4,285 | 16 | 9 | 7 | procedure/argument |

> `large-codebases` raw `grep` shows 13 `##`/`###`; four (`## Test structure`, `## Running tests`,
> `## Test utilities`, `## Patterns`, L322–L343) are **inside the SKILL.md code fence**, not page
> sections — the real structure is 9 H2 + 7 H3. Code-block count is by opening fences (3 / 16).

> **H2 lists (document order):**
> - **devcontainer**: Add Claude Code to your dev container · Persist authentication and settings across rebuilds · Enforce organization policy · Restrict network egress · Run without permission prompts · Try the reference container · Next steps (plus the lead "How dev containers work with your editor" accordion + the security `Warning` callout before the first H2)
> - **large-codebases**: What this guide covers (H3 Settings on this page, The example monorepo) · Choose where to start Claude · Layer CLAUDE.md files by directory (H3 Choose between per-directory CLAUDE.md and path-scoped rules, Exclude irrelevant CLAUDE.md files) · Reduce what Claude reads (H3 Block reads of generated and vendored code, Reduce file reads with code intelligence) · Scope worktrees and file access (H3 Check out only the directories you need, Grant access across packages or repositories) · Add per-directory skills (H3 Keep skills discoverable) · Centralize conventions when layering stops scaling (H3 Recommend the right plugin at session start) · Put it together · Scope and plan changes that span packages · Next steps

## Planned Notes (LOCKED)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **6 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_devcontainer_setup.md` | procedure | devcontainer: how-it-works accordion, Add Claude Code (3 Steps), auth-prompt, Try the reference container, Next steps | 600 | How dev containers wrap Claude Code (host editor + Docker container, bind-mounted workspace); install via the Dev Container Feature in `devcontainer.json`; rebuild; sign in (Anthropic vs cloud-provider creds); the 3-file reference container. Sandbox comparison → B05B; cloud creds → B14A. |
| 2 | `cc_devcontainer_hardening.md` | procedure | devcontainer: Warning callout, Persist auth across rebuilds, Enforce organization policy, Restrict network egress, Run without permission prompts | 650 | Hardening a dev container: persist `~/.claude` via a named volume / `CLAUDE_CONFIG_DIR` / Codespaces secret; push `managed-settings.json` + `containerEnv` policy; restrict egress with `init-firewall.sh` (`NET_ADMIN`/`NET_RAW`); when `--dangerously-skip-permissions` is acceptable (non-root, confined) and its risks. Managed-settings keys → B03A; permission modes → B05A. |
| 3 | `cc_large_codebase_strategy.md` | argument | large-codebases: intro, What this guide covers (+ Settings table, example monorepo), Choose where to start Claude, Scope and plan changes that span packages, Next steps | 600 | Why defaults degrade as a codebase grows (context fills with unrelated instructions + file reads); the layering principle (independent settings that combine); root-vs-subdirectory launch trade-off; sequencing cross-package changes (one session + saved plan that survives compaction). Settings details → notes 4–6. |
| 4 | `cc_large_codebase_claude_md_layering.md` | procedure | large-codebases: Layer CLAUDE.md files by directory (+ Choose between per-directory CLAUDE.md and path-scoped rules, Exclude irrelevant CLAUDE.md files) | 600 | Per-directory CLAUDE.md (root-wide rules + per-package/subsystem conventions, on-demand load); keeping them current (PR review, post-model-release pruning, Stop-hook proposer); per-directory CLAUDE.md vs path-scoped `.claude/rules/`; `claudeMdExcludes` glob patterns and scope merging. CLAUDE.md loading internals → B02B. |
| 5 | `cc_large_codebase_reduce_reads_and_worktrees.md` | procedure | large-codebases: Reduce what Claude reads (Block reads of generated/vendored code, Reduce file reads with code intelligence), Scope worktrees and file access (Check out only the directories you need, Grant access across packages or repositories) | 650 | Cutting file-read context: `.gitignore`-respecting search + `Read` deny rules for checked-in artifacts; code-intelligence (LSP) plugins instead of file scans; `worktree.sparsePaths` + `symlinkDirectories` for lightweight (sub)agent worktrees; `additionalDirectories` / `--add-dir` cross-package access and the CLAUDE.md/skills load matrix. Permission rule syntax → B05A; worktree ref → B10B. |
| 6 | `cc_large_codebase_skills_and_plugins.md` | procedure | large-codebases: Add per-directory skills (+ Keep skills discoverable), Centralize conventions when layering stops scaling (+ Recommend the right plugin at session start), Put it together | 600 | Per-directory `.claude/skills/` and `paths`-scoped skills that load on demand; keeping the skill list small + descriptions that survive shortening + OTel `skill_activated` audit; promoting drifting per-directory CLAUDE.md into skills/plugins/MCP for central governance; SessionStart-hook plugin recommender; the combined `packages/api/` configuration. Skills/plugins ref → B06/B09; hooks → B07A. |

**Estimate: 6 notes** — procedure ×5 (notes 1,2,4,5,6), argument ×1 (note 3). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (6,376 words). New `cc_` notes: 6. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~3,700 (avg ~617/note). Code blocks: ≤6 per note (source has 3 + 16; digest
  copies only the load-bearing config snippets, never all 19).
- **Building Block Distribution**: procedure ×5 (notes 1,2,4,5,6) · argument ×1 (note 3). No
  concept/model/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (15 distinct `term_dictionary/` terms across

## Per-Note Related Notes Mapping (LOCKED)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_devcontainer_setup` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agentic coding tool whose container install this note documents; the dev-container feature installs the Claude Code CLI + VS Code extension and the `claude` command runs inside the container.
- [Sandbox — Isolated Execution Environment](../../term_dictionary/term_sandbox.md) — A dev container is one form of isolated execution environment: commands Claude runs execute inside the container rather than on the host, which is exactly the sandbox-isolation property this note relies on.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note explains the same Claude Code harness (tools, terminal, `~/.claude` config) runs identically inside the container regardless of editor, so the harness term grounds what gets installed and configured.
- [VS Code](../../term_dictionary/term_vscode.md) — VS Code is the worked example throughout the install steps (Command Palette "Rebuild Container", the Claude Code extension panel vs integrated terminal), so the term grounds the primary editor surface.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — The Docker-container-on-a-host-or-cloud model the note describes (local or GitHub Codespaces) is the container-backend execution substrate this term defines, contextualizing where the isolated environment runs.
- [RDE - Rapid Development Environment](../../term_dictionary/term_rde.md) — RDE is the internal analog of a reproducible, identical-per-engineer dev environment, contextualizing the "every engineer runs the same image" benefit this note's dev-container setup delivers.

### 2. `cc_devcontainer_hardening` (7 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note's "Run without permission prompts" section is precisely a graduated-trust decision: when the container's isolation justifies dropping prompts (`--dangerously-skip-permissions`) vs keeping a classifier (auto mode), the trade-off this term frames.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — The egress-restriction section blocks all outbound traffic except an allowlist of required domains — the default-deny posture this term defines, applied at the container network layer.
- [Sandbox — Isolated Execution Environment](../../term_dictionary/term_sandbox.md) — Hardening only makes sense because the container is an isolated execution environment; the note pairs `--dangerously-skip-permissions` with network egress limits to keep a bypassed session's reach inside the sandbox boundary.
- [Blast Radius - Failure Impact Scope](../../term_dictionary/term_blast_radius.md) — The Warning callout and the no-prompts section are about limiting what a malicious project can exfiltrate or reach — explicitly reducing the blast radius of a bypassed or compromised session.
- [AWS Secrets Manager](../../term_dictionary/term_secrets_manager.md) — The note's credential guidance (don't mount `~/.ssh` or cloud credential files; prefer repository-scoped/short-lived tokens or `containerEnv`/Codespaces secrets) is the secrets-handling discipline this term anchors.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The hardening targets (`~/.claude` persistence, `managed-settings.json`, `containerEnv`, the bypass flag) are all Claude Code's own configuration surfaces, so the product term grounds what is being secured.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Enforcing `managed-settings.json` and `containerEnv` (telemetry opt-out, auto-update disable, MCP allowlists) at the highest settings precedence is deliberate control over what loads into and runs in every session — an instance of context/configuration engineering.

### 3. `cc_large_codebase_strategy` (8 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — The whole guide's premise is that a large codebase's defaults fill the context window with unrelated instructions and file reads; this strategy note frames every later setting as a context-window-budget decision.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Scoping Claude to only the part of the codebase a task touches — choosing what instructions and files enter context — is exactly the context-engineering discipline this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the strategic overview for configuring Claude Code itself in a monorepo/large tree, so the product term defines the host whose launch directory and settings are being scoped.
- [Compaction](../../term_dictionary/term_compaction.md) — The "scope and plan changes" section advises saving the plan to a file because a long cross-package session compacts its context along the way and the conversation history may not survive — the compaction behavior this term explains.
- [Subagent](../../term_dictionary/term_subagent.md) — The note's Tip recommends running exploration in a subagent so file reads stay out of the main conversation, the context-isolation technique this term defines and a core large-codebase strategy.
- [Skills](../../term_dictionary/term_skills.md) — The settings table previews per-directory skills as one of the layering mechanisms; the strategy note frames skills as on-demand instructions that keep context small, motivating note 6.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — Per-directory CLAUDE.md files are the persistent project-instruction layer this guide reorganizes; agentic memory is the mechanism by which those committed conventions persist and load across sessions.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The guide tunes an autonomous coding agent to operate effectively at scale (millions of lines / many packages) without degrading — the scaling behavior of the agent category this term defines.

### 4. `cc_large_codebase_claude_md_layering` (6 term notes)
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — Per-directory CLAUDE.md files are Claude Code's project-memory mechanism; this note documents how layering them (root + per-subdirectory) controls what persistent instruction memory loads, the core of agentic memory.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's motivation is that a single root CLAUDE.md grows to cover every subsystem and costs context on unrelated instructions; layering + `claudeMdExcludes` is a direct context-window economy.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Deciding which conventions load where (per-directory files, path-scoped rules, exclusions, scope merging) is a precise act of engineering what enters context, the discipline this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — CLAUDE.md, `.claude/rules/`, `claudeMdExcludes`, and the settings scopes are all Claude Code configuration surfaces, so the product term grounds the files this note configures.
- [Skills](../../term_dictionary/term_skills.md) — The "choose between" guidance and the cross-link to Compare-similar-features position CLAUDE.md against skills/rules as alternative instruction-delivery mechanisms, so the skills term frames the comparison this note makes.
- [Workflow Memory](../../term_dictionary/term_workflow_memory.md) — Maintaining per-area conventions in versioned CLAUDE.md files (PR review, post-model-release pruning, Stop-hook proposer) is a workflow-memory pattern: encoding repeatable procedural knowledge that persists with the code.

### 5. `cc_large_codebase_reduce_reads_and_worktrees` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — File reads are the second context cost the guide attacks; deny rules, code-intelligence lookups, and sparse worktrees all exist to keep irrelevant content out of the context window this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The `worktree.sparsePaths` setting is highlighted for subagent worktree isolation — parallel Claude instances each getting a lightweight checkout — the subagent fan-out pattern this term defines.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — The `Read` deny rules in `permissions.deny` block opening generated/vendored files even when search lists them — an explicit deny-list applied to the file-read surface, the posture this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `additionalDirectories` / `--add-dir` and `Read` deny rules tune exactly which paths Claude may read and write across packages — the scoped, settings-driven access control this term frames.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `permissions.deny`, `worktree.sparsePaths`/`symlinkDirectories`, `additionalDirectories`, `--add-dir`, and code-intelligence plugins are all Claude Code settings/flags, so the product term grounds what this note configures.
- [Skills](../../term_dictionary/term_skills.md) — Code-intelligence is delivered as a plugin and the `--add-dir` load matrix governs whether an added directory's skills load, so the skills term contextualizes the extension surfaces this note's settings interact with.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Replacing exhaustive file scans with language-server lookups and pruning reads to relevant paths is engineering what content reaches the model — the context-engineering discipline this term defines.

### 6. `cc_large_codebase_skills_and_plugins` (7 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note is about per-directory `.claude/skills/` and `paths`-scoped skills that load on demand, so the skills term is the central concept it documents (placement, descriptions, namespacing, discoverability).
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — The note writes `SKILL.md` with `name`/`description`/`paths` frontmatter and explains description-shortening — the skill-manifest format this term defines and the field whose keywords must survive truncation.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — When per-directory CLAUDE.md stops scaling, the note packages conventions as a versioned plugin with `plugin-name:skill-name` namespacing, the plugin-bundle structure this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — The motivation is that only a chosen skill's full content loads while names/descriptions always load, and a sprawling skill list eats context — the context-budget reasoning this term anchors.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The "centralize conventions" section recommends exposing an existing code-search/RAG index as an MCP tool so Claude queries it instead of reading files — the external-tool integration this term defines.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — The SessionStart-hook plugin-recommender that reads the launch directory and injects the right plugin recommendation before the first prompt is a lightweight orchestration/routing mechanism this term frames.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Moving always-loaded CLAUDE.md content into on-demand skills/plugins/MCP and keeping descriptions lean is deliberate control of what loads when — the context-engineering discipline this term defines.

## Section Coverage Map

```
devcontainer.md
├── (lead) How dev containers work with editor (accordion) → note 1 (cc_devcontainer_setup)
├── (lead) Security Warning callout ──────────────────────── → note 2 (cc_devcontainer_hardening)
├── Add Claude Code to your dev container (3 Steps) ──────── → note 1
│   └── auth-prompt (Anthropic vs cloud provider) ───────── → note 1 (cloud creds → B14A link)
├── Persist authentication and settings across rebuilds ─── → note 2
├── Enforce organization policy ──────────────────────────── → note 2 (managed-settings keys → B03A; admin → B14B)
├── Restrict network egress ──────────────────────────────── → note 2 (network domains → B14B network-config)
├── Run without permission prompts ───────────────────────── → note 2 (permission modes/auto mode → B05A)
├── Try the reference container (3 files table) ──────────── → note 1
└── Next steps (cards) ──────────────────────────────────── → notes 1/2 (links); sandbox compare → B05B
large-codebases.md
├── (intro) why defaults degrade at scale ────────────────── → note 3 (cc_large_codebase_strategy)
├── What this guide covers ───────────────────────────────── → note 3
│   ├── Settings on this page (table) ───────────────────── → note 3 (table previews notes 4–6)
│   └── The example monorepo (tree) ────────────────────── → note 3 (shared layout reused by 4–6)
├── Choose where to start Claude ─────────────────────────── → note 3 (root vs subdir trade-off)
├── Layer CLAUDE.md files by directory ───────────────────── → note 4 (cc_large_codebase_claude_md_layering)
│   ├── Choose between per-dir CLAUDE.md and path-scoped rules → note 4 (memory internals → B02B)
│   └── Exclude irrelevant CLAUDE.md files (claudeMdExcludes) → note 4
├── Reduce what Claude reads ─────────────────────────────── → note 5 (cc_large_codebase_reduce_reads_and_worktrees)
│   ├── Block reads of generated and vendored code ──────── → note 5 (permission syntax → B05A)
│   └── Reduce file reads with code intelligence (LSP) ──── → note 5 (plugins → B09 discover-plugins)
├── Scope worktrees and file access ──────────────────────── → note 5
│   ├── Check out only the directories you need (sparsePaths) → note 5 (worktree ref → B10B/B03A)
│   └── Grant access across packages or repositories ─────── → note 5 (--add-dir; env var)
├── Add per-directory skills ─────────────────────────────── → note 6 (cc_large_codebase_skills_and_plugins)
│   └── Keep skills discoverable ────────────────────────── → note 6 (skills ref → B06; OTel → B15B)
├── Centralize conventions when layering stops scaling ───── → note 6 (skills/plugins/MCP → B06/B09/B08A)
│   └── Recommend the right plugin at session start (hook) ─ → note 6 (hooks → B07A/B07B)
├── Put it together (combined settings + tree) ───────────── → note 6
├── Scope and plan changes that span packages ────────────── → note 3 (compaction → B02A context-window)
└── Next steps (hooks/costs/blog) ────────────────────────── → notes 3/5/6 (links); costs → B02A
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| devcontainer (2.1Kw, 6 H2, setup + hardening mixed) | notes 1, 2 | distinct procedures: install/run (note 1) vs persist-auth/policy/egress/no-prompts hardening (note 2); the security `Warning` belongs with hardening, the how-it-works accordion with setup |
| large-codebases (4.3Kw >2500, 16 code blocks >6) | notes 3, 4, 5, 6 | exceeds BOTH word AND code-block caps; split by mechanism family — strategy/where-to-start (argument), CLAUDE.md layering, read-reduction + worktree scoping, skills + plugins — so each note ≤2500w and ≤6 code blocks |

## Density Re-Assessment (LOCKED)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_devcontainer_setup | procedure | 600 | 2 | ✅ (devcontainer.json + reference-files table; ≤6) |
| 2 | cc_devcontainer_hardening | procedure | 650 | 4 | ✅ (volume mount, managed-settings COPY, containerEnv, +1; ≤6) |
| 3 | cc_large_codebase_strategy | argument | 600 | 2 | ✅ (monorepo tree + where-to-start table; ≤6) |
| 4 | cc_large_codebase_claude_md_layering | procedure | 600 | 4 | ✅ (root CLAUDE.md, package CLAUDE.md, claudeMdExcludes, +1; ≤6) |
| 5 | cc_large_codebase_reduce_reads_and_worktrees | procedure | 650 | 6 | ✅ (deny rules, lsp shell, sparsePaths+symlink merged, additionalDirectories, --add-dir, env-var; =6 cap, monitor) |
| 6 | cc_large_codebase_skills_and_plugins | procedure | 600 | 5 | ✅ (mkdir, SKILL.md, plugin install shell, put-it-together settings, +1; ≤6) |

No note exceeds the caps. Note 5 sits AT the 6-code-block cap — during execution copy only the
load-bearing snippets (merge the two `sparsePaths` examples into one with `symlinkDirectories`; render the
`--add-dir` env-var variant inline as prose if it would push to 7) so it stays ≤6. No over-compression —
every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_devcontainer_setup cc_devcontainer_hardening cc_large_codebase_strategy cc_large_codebase_claude_md_layering cc_large_codebase_reduce_reads_and_worktrees cc_large_codebase_skills_and_plugins"
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

Single phase (6 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met (esp. note 5 ≤6 code); every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 6 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 6 notes RECEIVES ≥1 inbound link from an existing vault note outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB confirms in-degree ≥1 for all 6 after inlinks applied; no graph island | DB in-degree query post-finalization |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes → CREATE `0_entry_points/entry_claude_code_docs.md`),
this sub-plan **contributes its 6 rows** under an "Enterprise / Operations — Dev Containers & Large
Codebases" cluster + increments the BB-distribution counts (procedure +5, argument +1). The entry-point
back-link is added to each note at finalization (G8).

## Undigested Terms Plan (Step 2d)

B15A creates **no new `term_dictionary` notes** — neither source page is a glossary, and every capitalized
concept maps to an existing substantive term note (link) or its home sub-plan (Pattern B). **Step 2d
re-scan (2026-06-13):** re-read both pages scanning emphasis/tables/callouts/code for newly-surfaced terms:

| Surfaced term / concept | Disposition |
|---|---|
| Development container / dev container | doc concept folded into note 1 `cc_devcontainer_setup` (no standalone term; the [containers.dev] spec is external) |
| Dev Container Feature | folded into note 1 (Claude Code install mechanism) |
| Sparse checkout / `worktree.sparsePaths` | folded into note 5; concept anchored by `term_subagent` (worktree isolation) — worktree settings owned by B10B/B03A |
| Code intelligence / LSP plugin | owned by B03B (`tools-reference#lsp`) / B09 (`discover-plugins#code-intelligence`) per Pattern B — captured there, linked here |
| Managed settings / `managed-settings.json` | owned by B03A (`settings`) / B14B (`server-managed-settings`) — linked, not recreated |
| `claudeMdExcludes` / `additionalDirectories` / `Read` deny rules | settings keys, owned by B03A/B05A reference; folded into notes 4/5 as usage, not term notes |
| Bind mount / named volume / `containerEnv` / Codespaces secret | Docker/devcontainer vocabulary folded into notes 1/2; no vault term note warranted |
| `--dangerously-skip-permissions` / auto mode | permission-mode vocabulary owned by B05A — linked via `term_graduated_trust` |
| Egress firewall / `init-firewall.sh` / `NET_ADMIN`/`NET_RAW` | folded into note 2; network requirements owned by B14B — concept anchored by `term_deny_first` |

on each note's concepts; no existing `cc_*` doc note covers dev-containers or large-codebase configuration
(this sub-plan is the first), and the 15 term links above are existing substantive term notes (linked, not
recreated). **0 new B15A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B15A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these concepts duplicate existing notes?) was
performed: `term_sandbox`, `term_sandbox_backend`, `term_graduated_trust`, `term_deny_first`,
`term_context_window`, `term_context_engineering`, `term_subagent`, `term_skills`, `term_mcp`,
`term_agentic_memory`, `term_claude_code` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B15A** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source; copy only load-bearing config snippets (note 5 must stay ≤6). One BB
  per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase
  --autostash` first; no Claude co-author trailer). Reindex incrementally; verify `note_links` + 0 broken
  links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 require in-degree ≥1 for every note):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_sandbox.md` | note 1 (`cc_devcontainer_setup`) | sandbox term → dev-container as isolated execution environment |
| `term_dictionary/term_deny_first.md` | note 2 (`cc_devcontainer_hardening`) | default-deny term → container egress allowlist hardening |
| `term_dictionary/term_graduated_trust.md` | note 2 (`cc_devcontainer_hardening`) | trust term → when to skip permission prompts in a container |
| `term_dictionary/term_context_window.md` | note 3 (`cc_large_codebase_strategy`) | context-window term → large-codebase context-budget strategy |
| `term_dictionary/term_agentic_memory.md` | note 4 (`cc_large_codebase_claude_md_layering`) | memory term → per-directory CLAUDE.md layering |
| `term_dictionary/term_subagent.md` | note 5 (`cc_large_codebase_reduce_reads_and_worktrees.md`) | subagent term → sparse worktree isolation for subagents |
| `term_dictionary/term_skills.md` | note 6 (`cc_large_codebase_skills_and_plugins`) | skills term → per-directory skills + plugin centralization |
| `0_entry_points/entry_claude_code_docs.md` | notes 1–6 | series hub → all 6 B15A rows (added at finalization) |

## Follow-up Recommendations

- After the 6 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify
  in-degree ≥1 for each note — G7/G8); queue the 6 rows for `entry_claude_code_docs.md`;
  `/tessellum-check-broken-links`.
- Cross-link the dev-container notes (1,2) with B05B sandboxing notes and the large-codebase notes (3–6)
  with B02B memory, B03A settings, B10B worktrees, and B06/B09 skills/plugins once those sub-plans execute.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | DONE 2026-06-13 — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | READY (9/9) — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B15A, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read from `inbox/claude_code_docs/`; measured words match the
  master's figure (devcontainer 2,091 · large-codebases 4,285 = 6,376). Code-block count measured by
  opening fences (3 / 16); confirmed the four `## Test*`/`## Patterns`/`## Running tests` headings in
  large-codebases are inside the SKILL.md fence (L322–L343), not page sections → real structure 9 H2 + 7
  H3. No >1.5× under-estimate; the large-codebases split was forced by BOTH the word cap AND the 16-code-block cap.
- **Notes**: 6 (procedure 5, argument 1) — matches master estimate. Splits: devcontainer → 2;
  large-codebases → 4 (documented in Split Decisions).
- **Per-Note Related Notes Mapping (Step 8)**: 6–8 term notes per note (15 distinct `term_dictionary/`
  false positives (e.g. `term_ssrf_guard`, `term_ecs`, `term_vpc`, `term_iframe_sandbox`) discarded as not
  same-sense; kept only genuinely-relevant agentic/container/context/security terms.
- **Step 2d new-term scan**: surfaced dev-container / sparse-checkout / code-intelligence / managed-settings
  vocabulary → all routed to existing terms or home sub-plans (B03A/B05A/B09/B10B/B14B); **0 new B15A term captures**.
- **Sections added/confirmed during augment**: Content Strategy, Summary Statistics & BB Distribution,
  Validation Scripts (bash), G7/G8 Discoverability gate rows, Inlinks table (executed at finalization).
- **28-item checklist**: PASS (term-note items N/A — B15A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented; review (below) sets `pending → ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8 incl G7/G8) | ✅ PASS | 8 gate rows present (single phase); G7/G8 Discoverability (inbound in-degree ≥1) included with Inlinks table executed at finalization. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B15A contributes 6 rows under an Enterprise/Operations cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 6 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`+`**Last Updated**`+`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | All 6 notes 600–650w. Note 5 sits AT the 6-code-block cap → flagged in Density Re-Assessment with a copy-only-load-bearing instruction to stay ≤6; no note exceeds caps. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: devcontainer 2,091 = plan 2,091; large-codebases 4,285 = plan 4,285; total 6,376 = master figure. Code blocks measured by opening fences (3 / 16). Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B15A authors 0 term notes; Step 2d scan + dedup across term_dictionary AND documentation/ documented; Authoring Requirements inherited (N/A). |
| CP9 | Term-slug specificity + collision audit (8.5f) | ✅ PASS | N/A (0 new slugs); concept-collision check documented (11 existing terms linked, not recreated; no existing `cc_*` doc note covers this topic). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.

**Source**: https://code.claude.com/docs/en/devcontainer , https://code.claude.com/docs/en/large-codebases
**Last Updated**: 2026-06-13
**Status**: Ready
