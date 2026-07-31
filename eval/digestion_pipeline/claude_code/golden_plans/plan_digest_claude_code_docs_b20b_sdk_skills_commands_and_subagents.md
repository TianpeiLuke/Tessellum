---
title: Sub-Plan B20B — Claude Code Docs: SDK Skills, Commands & Subagents
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/skills", "agent-sdk/slash-commands", "agent-sdk/subagents", "agent-sdk/plugins"]
---

# Sub-Plan B20B: SDK Skills, Commands & Subagents

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 Agent-SDK extensibility pages that explain how to load and invoke **Skills**, **slash commands**,
**subagents**, and **plugins** from a Claude Agent SDK application (the programmatic/`query()`-option layer,
distinct from the CLI/interactive treatment of the same primitives owned by B06/B07/B09/B10). P2 (Phase B) —
built on the P1 cores (skills, subagents, MCP, hooks) it references. Each page is the SDK-side companion to
a CLI-side doc page that lives in another sub-plan, so this sub-plan documents the **SDK option/parameter
surface** and links the conceptual/CLI pages rather than re-digesting them.

**Source**: Claude Code Agent SDK docs (`code.claude.com/docs/en/agent-sdk`), 4 pages, 8,101 measured words. **Planned: 6 notes.**

## Content Strategy

- **Prioritize**: the SDK option/parameter surfaces a developer programs against — `skills` option,
  `agents` parameter + `AgentDefinition` fields, `plugins` option, slash-command dispatch through the
  prompt string. These are what an SDK app author needs and cannot get from the CLI pages.
- **Group**: keep each page's distinct primitive as its own note where the SDK surface is self-contained
  (skills option, plugins option, slash-command dispatch). Split the large `subagents` page (3,659 w, 11
  H2, 14 H3) into the **declarative model** (`AgentDefinition` + benefits + inheritance + tool restrictions)
  vs the **runtime lifecycle** (invocation / detection / resuming / dynamic-workflow scale-up).
- **Skip / link-out (own other sub-plans)**: the conceptual Skill/Subagent/Plugin/Command CLI pages →
  B06 (`skills.md`/`commands.md`), B09A (`plugins.md`/`plugins-reference.md`), B10A (`sub-agents.md`,
  `agents.md`); dynamic-workflow orchestration page → B10B (`workflows.md`); SDK sessions/resume →
  B19B (`sessions.md`); SDK custom tools/MCP option → B20A; SDK Python/TypeScript option references →
  B21B/B21C. These are referenced via links, never duplicated.
- **Glossary / new terms**: 0 new `term_dictionary` captures — SDK primitives map to existing term notes
  (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read in full from `inbox/claude_code_docs/agent-sdk/` (verbatim mirror of
`code.claude.com/docs/en/agent-sdk/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| skills | /agent-sdk/skills | 1,479 | 8 | 9 | 5 | procedure |
| slash-commands | /agent-sdk/slash-commands | 1,585 | 10 | 5 | 8 | procedure |
| subagents | /agent-sdk/subagents | 3,659 | 5 | 11 | 14 | concept + procedure |
| plugins | /agent-sdk/plugins | 1,378 | 6 | 9 | 7 | procedure |

> Code counts are `<CodeGroup>` example blocks (Python+TypeScript pairs counted as the displayed examples,
> not raw fences). H2 counts exclude the in-fence `##` headings that appear inside `slash-commands` command-file
> code examples (`## Context`, `## Task`, `## Changed Files`, `## Detailed Changes`, `## Review Checklist` are
> sample-file contents, not page sections) — real H2s: 5.

> **H2 lists (document order):**
> - **skills**: Overview · How Skills Work with the SDK · Using Skills with the SDK · Skill Locations · Creating Skills · Tool Restrictions · Discovering Available Skills · Testing Skills · Troubleshooting (H3 Skills Not Found, Skill Not Being Used, Additional Troubleshooting) · Related Documentation (H3 Skills Guides, SDK Resources)
> - **slash-commands**: (intro) · Discovering Available Slash Commands · Sending Slash Commands · Common Slash Commands (H3 `/compact`, `/clear`) · Creating Custom Slash Commands (H3 File Locations, File Format, Using Custom Commands in the SDK, Advanced Features, Organization with Namespacing, Practical Examples) · See Also
> - **subagents**: Overview · Benefits of using subagents (H3 Context isolation, Parallelization, Specialized instructions and knowledge, Tool restrictions) · Creating subagents (H3 Programmatic definition, AgentDefinition configuration, Filesystem-based definition) · What subagents inherit · Invoking subagents (H3 Automatic invocation, Explicit invocation, Dynamic agent configuration) · Detecting subagent invocation · Resuming subagents · Tool restrictions (H3 Common tool combinations) · Scale up with dynamic workflows · Troubleshooting (H3 Claude not delegating, Filesystem-based agents not loading, Windows long prompt failures) · Related documentation
> - **plugins**: What are plugins? · Loading plugins (H3 Path specifications) · Verifying plugin installation · Using plugin skills · Complete example · Plugin structure reference · Common use cases (H3 Development and testing, Project-specific extensions, Multiple plugin sources) · Troubleshooting (H3 Plugin not loading, Skills not appearing, Path resolution issues) · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **6 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_skills.md` | procedure | skills: How Skills Work, Using Skills, Skill Locations, Creating Skills, Tool Restrictions, Discovering, Testing, Troubleshooting | 650 | Loading filesystem Skills into a `query()` session: `setting_sources`/`settingSources` discovery, the `skills` option (`"all"`/list/`[]`), auto-add of `Skill` tool to `allowedTools`, SDK `allowedTools` tool-restriction (SKILL.md `allowed-tools` ignored in SDK), troubleshooting. Concept of a Skill → `term_skills` / B06 `cc_skills`. |
| 2 | `cc_sdk_slash_commands.md` | procedure | slash-commands: intro, Discovering, Sending, Common (`/compact`,`/clear`), Creating Custom, Advanced Features, Namespacing, Practical Examples | 600 | Dispatching slash commands through the SDK prompt string; `system/init` `slash_commands` discovery; built-ins `/compact` (compact_boundary) & `/clear`; custom commands as `.claude/commands/*.md` (legacy; prefer `.claude/skills/`) with frontmatter, `$0/$1/$ARGUMENTS`, `!` bash, `@` file refs, subdir namespacing. ≤6 code blocks (split source). |
| 3 | `cc_sdk_subagents_definition.md` | concept | subagents: Overview, Benefits (isolation/parallel/specialized/tool-restrict), Creating (programmatic, AgentDefinition table, filesystem), What subagents inherit, Tool restrictions | 750 | The declarative subagent model: 3 creation paths (programmatic `agents` param / filesystem `.claude/agents/` / built-in `general-purpose`); the full `AgentDefinition` field table; benefits; the inherit/not-inherit contract; tool-restriction patterns. Programmatic precedence over filesystem. |
| 4 | `cc_sdk_subagents_lifecycle.md` | procedure | subagents: Invoking (auto/explicit/dynamic), Detecting invocation, Resuming, Scale up with dynamic workflows, Troubleshooting | 650 | Runtime subagent lifecycle: auto vs explicit vs factory-built dynamic invocation; detecting via `Agent`/`Task` `tool_use` + `parent_tool_use_id`; resume via captured `session_id`+`agentId`; transcript persistence/cleanup; `Workflow` tool for hundreds of agents (→ B10B); troubleshooting (delegation, reload, Windows 8191-char limit). |
| 5 | `cc_sdk_plugins.md` | procedure | plugins: What are plugins, Loading plugins, Path specs, Verifying install, Using plugin skills, Complete example, Common use cases, Troubleshooting | 600 | Programmatically loading local plugins via the `plugins` option (`{type:"local", path}` only); verifying through `system/init` (`plugins`/`skills`/`slash_commands`); namespaced `/plugin:skill` invocation; relative/absolute path rules; dev/project/multi-source patterns; troubleshooting. |
| 6 | `cc_sdk_plugin_structure.md` | concept | plugins: Plugin structure reference (directory layout + optional manifest) | 350 | What a loadable plugin directory contains: optional `.claude-plugin/plugin.json` manifest (auto-discovery when omitted), `skills/`, `commands/` (legacy), `agents/`, `hooks/`, `.mcp.json`; the four extension component types (skills/agents/hooks/MCP). Full plugin-dev/schema → B09A. |

**Estimate: 6 notes** — procedure ×4 (notes 1,2,4,5), concept ×2 (notes 3,6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (8,101 words). New `cc_` notes: 6. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~3,600 (avg ~600/note). Code blocks: ≤6 per note (source is example-heavy; each note keeps only the load-bearing Python/TypeScript option snippet(s), verbatim).
- **Building Block Distribution**: procedure ×4 (notes 1,2,4,5) · concept ×2 (notes 3,6). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> false positives discarded (e.g. `term_fan_out` = SNS/Kinesis messaging, NOT agent fan-out → dropped).

### 1. `cc_sdk_skills` (6 term notes)
- [Skills](../../term_dictionary/term_skills.md) — Defines the Skill primitive (SKILL.md + description, model-invoked); this note is the SDK-loading procedure for exactly that primitive, so the term is its definitional anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note configures Skills inside a Claude Agent SDK `query()` session; Claude Code is the harness/product whose `skills` and `settingSources` options the note programs against.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Skill discovery, the auto-added `Skill` tool, and `allowedTools` gating are all harness wiring; the term explains the engine that loads filesystem Skills and exposes them to the model.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The note's discovery note points to the `plugins` option as an alternative skill source and contrasts Skills (knowledge) with MCP (external tools), the sibling extension mechanism a developer chooses between.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Setting the `skills` option auto-adds the `Skill` tool to `allowedTools`, and tool restriction is the note's core control surface — i.e. the function-calling/tool-use mechanism by which the model actually invokes a Skill.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Skills load metadata at startup and full content only when triggered (the `skills` option is "a context filter, not a sandbox"); this lazy-load discipline is exactly the context-engineering trade-off the note documents.

### 2. `cc_sdk_slash_commands` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Slash commands control a Claude Code session through the SDK prompt string; Claude Code is the product whose `system/init` `slash_commands` list and dispatch behavior the note documents.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — A custom slash command encapsulates an operation as a standalone markdown object (with frontmatter, args, bash/file refs) that the SDK queues and dispatches by name — the GoF "encapsulate a request as an object" intent this term defines.
- [Compaction](../../term_dictionary/term_compaction.md) — The note's flagship built-in `/compact` command triggers history summarization and emits a `compact_boundary` event with pre-token counts; the term defines that exact context-reduction mechanism.
- [Context Window](../../term_dictionary/term_context_window.md) — `/clear` resets context to empty and `/compact` shrinks it; both built-in commands the note covers operate directly on the session's context window, the resource the term defines.
- [Skills](../../term_dictionary/term_skills.md) — The note's key migration guidance is that `.claude/commands/` is legacy and `.claude/skills/<name>/SKILL.md` is the recommended format supporting the same `/name` invocation, so Skills are the successor primitive a command author should know.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Custom commands declare `allowed-tools` frontmatter (e.g. `Bash(git add *)`, `Read`, `Grep`) gating which tools the command may invoke — the tool-use access control this term covers.

### 3. `cc_sdk_subagents_definition` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — This note defines the SDK subagent model (creation paths, `AgentDefinition` fields, inheritance, tool restrictions); the term is its canonical definitional anchor.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — The note's core "context isolation" benefit and the inherit/not-inherit table are exactly the sidechain-transcript mechanism: each subagent runs in a fresh isolated transcript and only its final message returns to the parent.
- [Agent-as-a-Tool](../../term_dictionary/term_agent_as_a_tool.md) — Subagents are invoked through the `Agent` tool with their own `description`/`prompt`/`tools`, i.e. a specialized agent wrapped as a callable tool the orchestrator delegates to — the pattern this term names.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note programs the Claude Agent SDK `agents` parameter and `AgentDefinition` schema; Claude Code is the harness whose subagent definition surface the note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Tool inheritance, model override, skill preloading, and the fresh-context guarantee are all harness behaviors; the term explains the engine that instantiates a subagent from an `AgentDefinition`.
- [Context Window](../../term_dictionary/term_context_window.md) — The "context isolation" benefit the note leads with is precisely that a subagent's exploration never accumulates in the parent's context window; the term defines that bounded resource.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The `tools`/`disallowedTools` fields and the common-tool-combinations table restrict which tools a subagent may call — the tool-use access control this term covers.

### 4. `cc_sdk_subagents_lifecycle` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — This note covers the runtime subagent lifecycle (invocation, detection, resume, persistence); the term is its definitional anchor.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — The note's auto/explicit/dynamic invocation, detecting `parent_tool_use_id` provenance, and the `Workflow`-tool scale-up are orchestration controls — how a main agent coordinates and dispatches delegated workers, the patterns this term enumerates.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — The "scale up with dynamic workflows" section moves from a few delegated subagents per turn to coordinating dozens-to-hundreds of agents; the term defines that multi-agent operating regime.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — Resuming relies on subagent transcripts persisting in separate files unaffected by main-conversation compaction and cleaned up per `cleanupPeriodDays` — exactly the isolated sidechain transcript this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's `Agent`/`Task` tool naming, `agentId` trailer, and `resume` session option; Claude Code is the harness whose runtime behavior it describes.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Detecting invocations, summarizing the subagent's final message into a tool_result, and resuming a stored transcript are harness responsibilities; the term explains the engine that runs the lifecycle.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's persistence rules turn on subagent transcripts being unaffected when the main conversation compacts (separate context windows), and the `Workflow` tool exists to keep orchestration out of the conversation context — the resource this term defines.

### 5. `cc_sdk_plugins` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note programs the Claude Agent SDK `plugins` option to extend Claude Code with packaged functionality; Claude Code is the product whose plugin-loading surface it documents.
- [Skills](../../term_dictionary/term_skills.md) — Plugin skills are the primary loadable component the note demonstrates, invoked namespaced as `/plugin:skill` and surfaced in the `system/init` `skills` list; Skills are the central plugin payload.
- [Subagent](../../term_dictionary/term_subagent.md) — Agents/subagents are one of the four component types a loaded plugin contributes (skills, agents, hooks, MCP servers); the term defines that component.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — MCP servers are one of the four plugin component types (`.mcp.json`); a loaded plugin can add external tool integrations via MCP, the mechanism this term defines.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — Verifying a load checks the `system/init` `plugins`/`skills`/`slash_commands` lists and the note's troubleshooting validates `plugin.json`; the term explains the on-disk manifest that declares a plugin's identity/compatibility to the host loader.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Loading local plugins, namespacing their skills/commands, and surfacing them in the init message are harness responsibilities; the term explains the engine that resolves a plugin path and wires its components into the session.

### 6. `cc_sdk_plugin_structure` (6 term notes)
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — This note's subject is the plugin directory layout whose optional `.claude-plugin/plugin.json` IS the plugin manifest; the term defines that declaration and the auto-discovery fallback when it is omitted.
- [Skills](../../term_dictionary/term_skills.md) — `skills/<name>/SKILL.md` is the primary (non-legacy) component directory in the plugin layout the note describes; Skills are the recommended plugin payload.
- [Subagent](../../term_dictionary/term_subagent.md) — `agents/` is one of the four component directories in the plugin structure; it contributes custom subagents, the primitive this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — `.mcp.json` is the plugin component that declares MCP servers — external tool integrations via Model Context Protocol, the mechanism this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The directory layout and auto-discovery rules are how Claude Code resolves a plugin's components; the product term anchors what the structure plugs into.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Auto-discovering components from the directory layout (skills/commands/agents/hooks/MCP) when no manifest is present is harness loader behavior; the term explains the engine that reads the structure.

## Section Coverage Map

```
agent-sdk/skills.md
├── Overview ────────────────────────────── → note 1 (intro) + link term_skills / B06 cc_skills (concept)
├── How Skills Work with the SDK ─────────── → note 1 (cc_sdk_skills)
├── Using Skills with the SDK ────────────── → note 1
├── Skill Locations ──────────────────────── → note 1
├── Creating Skills ──────────────────────── → note 1 (summary) → linked out (B06 skills.md, full SKILL.md guide)
├── Tool Restrictions ────────────────────── → note 1
├── Discovering Available Skills ─────────── → note 1
├── Testing Skills ───────────────────────── → note 1
├── Troubleshooting (3 H3) ───────────────── → note 1
└── Related Documentation (2 H3) ─────────── → note 1 (links) → B06 / B20A / B20B siblings
agent-sdk/slash-commands.md
├── (intro: dispatchable commands) ───────── → note 2 (cc_sdk_slash_commands)
├── Discovering Available Slash Commands ─── → note 2
├── Sending Slash Commands ───────────────── → note 2
├── Common Slash Commands (/compact,/clear) ─ → note 2
├── Creating Custom Slash Commands ───────── → note 2
│   ├── File Locations / File Format ─────── → note 2
│   ├── Using Custom Commands in the SDK ─── → note 2
│   ├── Advanced Features (args/bash/@) ──── → note 2
│   ├── Organization with Namespacing ────── → note 2
│   └── Practical Examples ────────────────── → note 2 (representative subset)
└── See Also ─────────────────────────────── → note 2 (links) → B06 commands.md (full custom-command guide)
agent-sdk/subagents.md
├── Overview (3 creation ways) ───────────── → note 3 (cc_sdk_subagents_definition)
├── Benefits (4 H3) ──────────────────────── → note 3
├── Creating subagents ───────────────────── → note 3
│   ├── Programmatic definition ──────────── → note 3
│   ├── AgentDefinition configuration ────── → note 3 (full field table)
│   └── Filesystem-based definition ──────── → note 3 (summary) → linked out (B10A sub-agents.md)
├── What subagents inherit ───────────────── → note 3
├── Tool restrictions (+ combinations) ───── → note 3
├── Invoking subagents (auto/explicit/dyn) ─ → note 4 (cc_sdk_subagents_lifecycle)
├── Detecting subagent invocation ────────── → note 4
├── Resuming subagents ───────────────────── → note 4 (→ B19B sessions for resume-by-id)
├── Scale up with dynamic workflows ──────── → note 4 → linked out (B10B workflows.md)
├── Troubleshooting (3 H3) ───────────────── → note 4
└── Related documentation ────────────────── → notes 3/4 (links) → B10A / B10B
agent-sdk/plugins.md
├── What are plugins? (4 components) ──────── → note 5 (cc_sdk_plugins) + note 6
├── Loading plugins (+ Path specifications) ─ → note 5
├── Verifying plugin installation ────────── → note 5
├── Using plugin skills ──────────────────── → note 5
├── Complete example ─────────────────────── → note 5 (one consolidated example)
├── Plugin structure reference ───────────── → note 6 (cc_sdk_plugin_structure) → linked out (B09A plugins-reference.md)
├── Common use cases (3 H3) ──────────────── → note 5
├── Troubleshooting (3 H3) ───────────────── → note 5
└── See also ─────────────────────────────── → notes 5/6 (links) → B09A plugins.md / plugins-reference.md
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| subagents (3,659 w, 11 H2, 14 H3 — >2500 w cap) | notes 3 + 4 | exceeds density cap; clean BB seam — declarative *model* (concept: AgentDefinition, benefits, inheritance, tool restrictions) vs runtime *lifecycle* (procedure: invoke/detect/resume/scale/troubleshoot). |
| plugins (1,378 w) | notes 5 + 6 | within word cap but two BBs: the loading *procedure* (note 5) vs the static directory-structure *reference concept* (note 6, `## Plugin structure reference`). One BB per note rule forces the split. |
| skills (1,479 w, 8 code blocks) | note 1 (single) | within word/line caps; keep ≤6 code blocks by retaining only the load-bearing `skills`-option + tool-restriction snippets, citing the rest as prose. |
| slash-commands (1,585 w, ~10 example blocks) | note 2 (single) | within word/line caps; cap code at ≤6 by keeping discover/send/compact + 2 custom-command examples, summarizing the remaining practical examples as a bullet list. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_skills | procedure | 650 | 4 | ✅ |
| 2 | cc_sdk_slash_commands | procedure | 600 | 6 | ✅ |
| 3 | cc_sdk_subagents_definition | concept | 750 | 2 | ✅ |
| 4 | cc_sdk_subagents_lifecycle | procedure | 650 | 3 | ✅ |
| 5 | cc_sdk_plugins | procedure | 600 | 4 | ✅ |
| 6 | cc_sdk_plugin_structure | concept | 350 | 1 | ✅ |

No note approaches the 2,500-word / 400-line caps; code-block count held ≤6 by keeping only load-bearing
Python/TypeScript snippets verbatim and summarizing the rest. No over-compression — every H2/H3 maps to a
note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_skills cc_sdk_slash_commands cc_sdk_subagents_definition cc_sdk_subagents_lifecycle cc_sdk_plugins cc_sdk_plugin_structure"
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

Single phase (6 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (esp. SDK option names: `skills`/`agents`/`plugins`/`setting_sources`) | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 6 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 6 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability(audit) | re-verify in-degree ≥1 after reindex; no graph islands in the cluster | DB in-degree re-query post-reindex |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 6 rows** under an "Agent SDK — Extensibility" cluster + increments the
BB-distribution counts (procedure ×4, concept ×2). The entry-point back-link is the inbound link that, with
the Inlinks table below, satisfies G7/G8.

## Undigested Terms Plan (Step 4e)

b20b creates **no new `term_dictionary` notes** — every SDK primitive on these 4 pages maps to an existing
substantive term note (link) or its conceptual home sub-plan (Pattern B):

| SDK term / primitive | Disposition |
|---|---|
| Skill (`skills` option, SKILL.md) | link `term_skills` (exists); concept owned by B06 `cc_skills` |
| Slash command (`/name`, dispatch) | link `term_command_pattern` (exists); concept owned by B06 `cc_commands` |
| Subagent / `AgentDefinition` / `agents` param | link `term_subagent` (exists); concept owned by B10A `cc_sub_agents` |
| Plugin (`plugins` option) / plugin.json | link `term_plugin_manifest` (exists); concept owned by B09A `cc_plugins` |
| Context isolation / sidechain | link `term_sidechain_transcript` (exists) |
| Agent-as-a-tool (`Agent` tool delegation) | link `term_agent_as_a_tool` (exists) |
| Dynamic workflow / `Workflow` tool / scale-up | link `term_agent_orchestration` + `term_multi_agent` (exist); page owned by B10B `workflows.md` |
| `/compact` / `/clear` / compaction | link `term_compaction` + `term_context_window` (exist) |
| MCP servers (plugin component) | link `term_mcp` (exists); owned by B08A / B20A |
| Hooks (plugin component) | owned by B07A/B07B / B20C (link there) |
| `allowedTools` / tool restriction / `disallowedTools` | link `term_function_calling` (exists) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/code
comments for newly-surfaced terms. Candidates examined and routed (NOT captured): `general-purpose`
subagent, `Explore`/`Plan` built-in agents, `agentId`, `parent_tool_use_id`, `compact_boundary`,
`cleanupPeriodDays`, `settingSources`/`setting_sources`, `effort` level, `background` task — all are SDK
fields/identifiers documented inline in the owning `cc_sdk_*` note (not standalone vocabulary needing a
term page) or owned by another sub-plan (effort→B03B, sessions/resume→B19B). **0 new B20B `term_dictionary`
captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B20B authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the SDK primitives duplicate existing notes?) was
performed: `term_skills`, `term_subagent`, `term_mcp`, `term_command_pattern`, `term_plugin_manifest`,
`term_sidechain_transcript`, `term_agent_as_a_tool`, `term_agent_orchestration`, `term_multi_agent`,
`term_compaction`, `term_context_window`, `term_function_calling`, `term_claude_code`, `term_agent_harness`,
`term_context_engineering` all exist → linked, not recreated. The `cc_sdk_*` doc notes themselves were
dedup-checked against the (empty) `documentation/claude_code/` folder and against `term_dictionary` — no
existing doc/term note documents the *SDK option surface* (existing terms define the concepts; these notes
document the programmatic API), so creating them does not duplicate (P0-class) any existing note.

## Term-Note Authoring Requirements

**N/A for b20b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- **Code blocks verbatim** — copy the Python/TypeScript option snippets exactly from the source; do not
  invent option names. Keep ≤6 code blocks per note (summarize extra examples as prose). One BB per note.
  Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_skills.md` | notes 1, 5, 6 | Skills term → SDK skills-loading procedure + plugin skills + plugin layout |
| `term_dictionary/term_subagent.md` | notes 3, 4 | subagent term → SDK subagent definition + lifecycle |
| `term_dictionary/term_command_pattern.md` | note 2 | command-pattern term → SDK slash-command dispatch |
| `term_dictionary/term_plugin_manifest.md` | notes 5, 6 | plugin-manifest term → SDK plugin loading + structure reference |
| `term_dictionary/term_sidechain_transcript.md` | notes 3, 4 | sidechain term → SDK subagent isolation + transcript persistence/resume |
| `term_dictionary/term_agent_orchestration.md` | note 4 | orchestration term → SDK subagent invocation + Workflow scale-up |
| `0_entry_points/entry_claude_code_docs.md` | notes 1–6 | series entry point → all 6 B20B rows (created pre-step; provides the guaranteed inbound link) |

## Follow-up Recommendations

- After the 6 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 6
  rows for `entry_claude_code_docs.md` under "Agent SDK — Extensibility"; `/tessellum-check-broken-links`.
- Post-execution cross-link the SDK notes to their CLI-side siblings once those land (B06 `cc_skills`/
  `cc_commands`, B09A `cc_plugins`, B10A `cc_sub_agents`, B10B `cc_workflows`) so the SDK ↔ CLI pairs are
  bidirectionally reachable.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-13** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-13** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B20B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/agent-sdk/`;
  measured words match the master's figure (skills 1,479 · slash-commands 1,585 · subagents 3,659 ·
  plugins 1,378 = 8,101). `subagents` at 3,659 w exceeds the 2,500-w cap → forced split into notes 3+4
  (documented in Split Decisions). No other >1.5× under-estimate.
- **Notes**: 6 (procedure 4, concept 2) — matches master estimate (6). Two splits documented (subagents by
  BB seam; plugins by BB seam — loading procedure vs structure-reference concept).
  each) per note's concepts; **6–7 relevancy-selected term notes per note** (15 distinct `term_dictionary/`
  was surfaced by BM25 for the subagent/workflow concepts and **discarded** as not-genuinely-relevant;
  `term_plugin_sdk` (OpenClaw-specific) discarded in favor of `term_plugin_manifest` (the on-disk plugin
  declaration concept that actually matches).
- **Step 2d new-term scan**: SDK identifiers/fields surfaced (`general-purpose`, `agentId`,
  `compact_boundary`, `settingSources`, `effort`, `background`, `cleanupPeriodDays`) → all documented
  inline in the owning note or owned by another sub-plan; **0 new B20B term captures**.
- **Sections added/confirmed during augment**: Content Strategy, Summary Statistics & BB Distribution,
  Validation Scripts (bash), Section Coverage Map (no orphans), Split Decisions, Density Re-Assessment,
  Inlinks table (executed at finalization for G7/G8), Undigested Terms Plan + Step 2d re-scan + 10.5f audit.
- **28-item checklist**: PASS (term-note items N/A — B20B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented and reviewed; set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B20B contributes 6 rows under "Agent SDK — Extensibility". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 6 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body (`## Overview` / source-mirrored H2 / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer) match the master Format Definition verbatim. |
| CP6 | Borderline density → split | ✅ PASS | subagents (3,659 w >2,500) split 3+4; plugins split 5+6 on BB seam; skills/slash-commands held ≤6 code blocks. No remaining borderline note. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` 2026-06-13: skills 1,479 · slash-commands 1,585 · subagents 3,659 · plugins 1,378 = 8,101 = master figure (±0%). H2/H3/code counts verified by grep. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B20B authors 0 term notes; Undigested Terms Plan routes every SDK primitive to an existing term / home sub-plan; Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); SDK-primitive collision check documented (15 existing terms linked not recreated; `cc_sdk_*` doc notes dedup-checked vs empty `documentation/claude_code/` and vs `term_dictionary` — document the API surface, not the concept, so no P0 duplication). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.

**Source**: https://code.claude.com/docs/en/agent-sdk/skills
**Last Updated**: 2026-06-13
**Status**: Ready
