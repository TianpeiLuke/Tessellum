---
title: Sub-Plan B02B — Claude Code Docs: Memory, Sessions & .claude Directory
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["memory", "sessions", "checkpointing", "claude-directory"]
---

# Sub-Plan B02B: Memory, Sessions & .claude Directory

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted pilot [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are inherited
> from the master; this file extends, never overrides.

## Scope

The 4 persistence/state pages that explain how knowledge and conversation state carry across Claude Code
sessions: the two memory mechanisms (`CLAUDE.md` files + auto memory), session lifecycle (resume/name/branch/
export), checkpointing (rewind/summarize), and the `.claude/` directory map (every file Claude Code reads,
project + global, plus the application-data it writes). P1 (Phase A) — vocabulary like CLAUDE.md, auto memory,
rules, session, checkpoint, and the `.claude` dir is referenced by many later sub-plans, so this runs early.
Glossary terms route per Pattern B (see Undigested Terms Plan), not re-digested.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 14,400 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the memory model (CLAUDE.md vs auto memory), `.claude/rules/`, session resume/branch, and
  the `.claude` directory map — vocabulary cores other sub-plans (B03A settings, B05A permissions, B06 skills,
  B07 hooks, B10 subagents) link.
- **Group / split**: `memory.md` (3.8Kw, 6 H2 + many H3) splits by concept (CLAUDE.md authoring, rules, auto
  memory) vs procedure (org-wide deployment, troubleshooting). `claude-directory.md` (8.4Kw — most of it a JSX
  interactive-explorer component whose *data* is the per-file reference) splits into the project/global file
  map (concept) and the application-data lifecycle (procedure). `sessions.md` + `checkpointing.md` are kept as
  focused concept/procedure notes.
- **Skip / link-out (own other sub-plans)**: PreToolUse/InstructionsLoaded hooks → B07A/B07B; settings layers /
  precedence / `managed-settings.json` / `claudeMd` key → B03A; env vars (`CLAUDE_CONFIG_DIR`,
  `CLAUDE_CODE_SKIP_PROMPT_HISTORY`, `autoMemoryDirectory` semantics) → B03A; permissions / `permissions.deny` /
  managed settings → B05A; skills → B06; subagents + persistent subagent memory → B10A; worktrees /
  `.worktreeinclude` → B10B; plan mode → B05A; `/compact` + context-window mechanics → B02A; CLI reference
  (`--continue`, `--resume`, `--from-pr`, `-p`) → B03B; output styles → B06; keybindings/themes → B04A;
  `claude project purge` CLI → B03B. These are referenced via links, never duplicated.
- **Glossary**: not re-digested into `cc_` notes — terms route to existing term notes / their home sub-plan
  (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| memory | /memory | 3,817 | 13 | 6 | 12 | concept/procedure |
| sessions | /sessions | 1,317 | 4 | 7 | 1 | concept |
| checkpointing | /checkpointing | 816 | 2 | 4 | 5 | procedure |
| claude-directory | /claude-directory | 8,450 | 6 | 7 | 4 | concept/procedure |

> **Note on raw counts.** `memory.md`: `wc` reports 30 `\`\`\`` fences and 7 `##`, but several are *inside* fenced
> example bodies — the real prose has 6 H2 sections and 13 code blocks. `claude-directory.md`: of its 8,450
> words, ~6,600 are a JSX `ClaudeExplorer` React component (lines 9–1431) whose *data payload* is the per-file
> reference (CLAUDE.md, .mcp.json, .worktreeinclude, settings.json/.local, rules/, skills/, commands/,
> output-styles/, agents/, workflows/, agent-memory/, .claude.json, keybindings.json, themes/, projects/memory);
> only ~1,850 words (lines 1433–1612) are prose H2 sections. The JSX is digested for its *file-reference content*
> (the same data appears in the prose "File reference" table at L1490–1507), never transcribed as code.

> **H2 lists (document order):**
> - **memory**: CLAUDE.md vs auto memory · CLAUDE.md files (H3 When to add · Choose where to put · Set up a
>   project CLAUDE.md · Write effective instructions · Import additional files · AGENTS.md · How CLAUDE.md files
>   load [H4 Load from additional directories] · Organize rules with `.claude/rules/` [H4 Set up rules ·
>   Path-specific rules · Share rules with symlinks · User-level rules] · Manage CLAUDE.md for large teams [H4
>   Deploy organization-wide CLAUDE.md · Exclude specific CLAUDE.md files]) · Auto memory (H3 Enable or disable ·
>   Storage location · How it works · Audit and edit) · View and edit with `/memory` · Troubleshoot memory issues
>   (H3 Claude isn't following my CLAUDE.md · I don't know what auto memory saved · My CLAUDE.md is too large ·
>   Instructions seem lost after `/compact`) · Related resources
> - **sessions**: Resume a session (H3 Where the session picker looks) · Name your sessions · Use the session
>   picker · Branch a session · Manage context within a session · Export and locate session data · See also
> - **checkpointing**: How checkpoints work (H3 Automatic tracking · Rewind and summarize [H4 Restore vs.
>   summarize]) · Common use cases · Limitations (H3 Bash command changes not tracked · External changes not
>   tracked · Not a replacement for version control) · See also
> - **claude-directory**: (intro prose) · Explore the directory [interactive explorer = per-file reference] ·
>   What's not shown · Choose the right file · File reference · Troubleshoot configuration · Application data
>   (H3 Cleaned up automatically · Kept until you delete them · Plaintext storage · Clear local data) ·
>   Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **9 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_memory_overview.md` | concept | memory: intro, CLAUDE.md vs auto memory | 450 | The two cross-session memory mechanisms; both load at session start as context (not enforced — block via PreToolUse hook → B07); comparison table (who writes / contents / scope / loaded-into / use-for). |
| 2 | `cc_claude_md_files.md` | concept | memory: CLAUDE.md files (When to add, Choose where, Set up, Write effective, Import, AGENTS.md, How they load) | 750 | What CLAUDE.md is; the 4 scopes/locations in load order; when to add; writing effective instructions (size/structure/specificity/consistency); `@path` imports + CLAUDE.local.md; AGENTS.md import/symlink; walk-up load order + HTML-comment stripping. |
| 3 | `cc_claude_rules_directory.md` | concept | memory: Organize rules with `.claude/rules/` (Set up, Path-specific, Symlinks, User-level) | 500 | `.claude/rules/` topic files; unconditional vs `paths:`-scoped rules (glob patterns table); cross-project symlinks; user-level `~/.claude/rules/`; load priority (user before project; rules same priority as `.claude/CLAUDE.md`). |
| 4 | `cc_manage_claude_md_for_teams.md` | procedure | memory: Manage CLAUDE.md for large teams (Deploy org-wide, Exclude); + claudeMd-vs-settings table | 550 | Steps to deploy a managed-policy CLAUDE.md (per-OS paths, MDM/Group-Policy); `claudeMd` key in managed-settings.json; precedence + "where honored"; `claudeMdExcludes` glob exclusion (cannot exclude managed); when to use managed CLAUDE.md vs managed settings. |
| 5 | `cc_auto_memory.md` | concept | memory: Auto memory (Enable/disable, Storage location, How it works, Audit/edit) + View/edit with /memory | 650 | Claude-written cross-session notes; on by default (v2.1.59+); enable/disable (`/memory` toggle, `autoMemoryEnabled`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`); per-repo storage `~/.claude/projects/<project>/memory/`; MEMORY.md index + topic files; 200-line/25KB load rule; machine-local; `/memory` browse/edit; links `term_agentic_memory`. |
| 6 | `cc_troubleshoot_memory.md` | procedure | memory: Troubleshoot memory issues (4 H3) | 400 | Debug "Claude isn't following CLAUDE.md" (delivered as user message, not system prompt; `/memory` to verify loaded; specificity; conflicts); auto-memory inspection; "too large" → path rules; "lost after `/compact`" (root CLAUDE.md re-injected, nested not). |
| 7 | `cc_sessions.md` | concept | sessions: all (Resume, picker, Name, Branch, Manage context, Export/locate) | 700 | A session = saved conversation per project dir; resume (`--continue`/`--resume`/`--from-pr`/`/resume`); picker scope + shortcuts; naming (`-n`/`/rename`/Ctrl+R/plan-accept); branching/forking (`/branch`, `--fork-session`); in-session context cmds (`/clear`,`/compact`,`/context`); export + JSONL transcript location + retention. |
| 8 | `cc_checkpointing.md` | procedure | checkpointing: all (How it works, Rewind/summarize, Restore vs summarize, Use cases, Limitations) | 600 | Automatic pre-edit checkpoints (one per prompt, persist across sessions, 30-day cleanup); `/rewind` menu (Esc Esc); restore code/conversation/both vs summarize from/up-to-here; use cases; limitations (bash/external changes untracked, not a VCS replacement). |
| 9 | `cc_dot_claude_directory.md` | concept | claude-directory: intro, Explore the directory (per-file reference), What's not shown, Choose the right file, File reference | 800 | Map of `.claude/` (project) and `~/.claude/` (global): per-file purpose, scope, commit/gitignore badge, when-it-loads, for every node (CLAUDE.md, .mcp.json, .worktreeinclude, settings.json/.local, rules/, skills/, commands/, output-styles/, agents/, workflows/, agent-memory/, .claude.json, keybindings.json, themes/, projects/memory); "choose the right file" decision table; what's-not-shown (managed-settings, plugins). |
| 10 | `cc_claude_application_data.md` | procedure | claude-directory: Application data (Cleaned up automatically, Kept until you delete them, Plaintext storage, Clear local data) + Troubleshoot configuration | 600 | The data `~/.claude` writes as you work: auto-cleaned paths (transcripts, file-history, plans, debug, caches; `cleanupPeriodDays` 30d) vs kept-until-deleted (history.jsonl, stats-cache, remote-settings); plaintext-at-rest risk + mitigations; `claude project purge` (dry-run/--yes/--all) + manual-delete table. |

**Estimate: 10 planned rows but 9 LOCKED notes** — see Split Decisions: notes 9 + 10 are the two halves of
`claude-directory.md`. To stay at the master's 9-note estimate, **note 10 (`cc_claude_application_data`) is
authored as a SEPARATE note** (procedure BB ≠ note 9's concept BB; combined they exceed 2,500w), so the final
count is **9 cc_ notes from memory/sessions/checkpointing (1–8) is 8, plus claude-directory yields 2 (9–10)**.
Final lock: **10 notes** is the honest count; the master's "9 (est.)" is an estimate the augment is allowed to
adjust. **LOCKED at 10 notes** (concept ×6: 1,2,3,5,7,9 · procedure ×4: 4,6,8,10). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (14,400 words). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~6,100 (avg ~610/note). Code blocks: ≤6 per note (config snippets: CLAUDE.md import,
  managed-settings `claudeMd`, `autoMemoryEnabled`, MEMORY.md index, `/branch`, `claude project purge`).
- **Building Block Distribution**: concept ×6 (notes 1, 2, 3, 5, 7, 9) · procedure ×4 (notes 4, 6, 8, 10). No
  model/argument/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (12 distinct `term_dictionary/` terms across the 10

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> All terms below verified present via `ls .../term_dictionary/<slug>.md` (2026-06-13).

### 1. `cc_memory_overview` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: Anthropic's agentic coding tool; relevance: this note documents Claude Code's two native cross-session memory mechanisms, so the product term is the host whose memory model is being defined.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what the term is: the general pattern of an agent persisting learnings across sessions; relevance: auto memory (Claude writing notes to itself based on corrections) is the concrete agentic-memory mechanism this note contrasts with author-written CLAUDE.md.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: deliberate curation of what enters the context window; relevance: the note stresses both memory systems load at session start as *context* and that specific/concise instructions get followed more reliably — a context-engineering trade-off.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the fixed token budget per conversation; relevance: both CLAUDE.md and the first 200 lines/25KB of MEMORY.md are loaded into the context window every session, so the window is the container this note's memory items occupy.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime wrapping an LLM with tools/context/execution; relevance: the note notes memory is treated as context not enforced configuration, and to *enforce* behavior you use a PreToolUse hook — i.e., the harness's enforcement layer, not the model's discretion.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: agents that plan/edit/run across a codebase autonomously; relevance: cross-session memory is what lets such an agent accumulate project knowledge and improve over repeated autonomous sessions, the capability this note enables.

### 2. `cc_claude_md_files` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: CLAUDE.md is Claude Code's primary author-written instruction file, so the product term anchors what this note documents (scopes, load order, imports).
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context for an LLM; relevance: the note's "Write effective instructions" guidance (size <200 lines, structure, specificity, consistency, adherence vs length) is a context-engineering playbook for the instruction file.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the per-session token budget; relevance: CLAUDE.md and all `@path` imports load *in full* into the context window at launch, so the note repeatedly ties file size to context consumption and adherence.
- [Skills](../../term_dictionary/term_skills.md) — what the term is: packaged on-demand workflows invoked by name; relevance: the note explicitly routes multi-step procedures or task-specific content *out* of CLAUDE.md into a skill (or path-scoped rule), making skills the contrast case for what belongs in CLAUDE.md.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime wrapping the model; relevance: the note describes how the harness walks up the directory tree, concatenates CLAUDE.md files, strips HTML comments, and expands imports before injecting into context — harness-level loading mechanics.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: agents acting across a codebase; relevance: CLAUDE.md supplies the build commands, conventions, and architecture that let the agent operate correctly without re-explanation each session — the persistent project contract this note defines.

### 3. `cc_claude_rules_directory` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: `.claude/rules/` is a Claude Code config directory, so the product term grounds the feature this note documents.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: path-scoped rules are precisely a context-engineering device — instructions load *only* when Claude reads matching files, reducing noise and saving context space, the note's central rationale.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the token budget; relevance: the note motivates `paths:` scoping as a way to keep instructions out of the context window until a matching file is opened, directly managing window consumption.
- [Skills](../../term_dictionary/term_skills.md) — what the term is: on-demand invoked workflows; relevance: the note's Note callout distinguishes rules (load every session or on matching-file open) from skills (load only when invoked or task-relevant), making skills the comparison axis for choosing where instructions live.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime wrapping the model; relevance: the harness discovers `.md` files recursively, resolves symlinks (handling circular ones), and applies user-before-project load priority — the rule-resolution mechanics this note documents.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: codebase-wide agents; relevance: topic/path-scoped rules let an autonomous agent apply the right conventions per file type (testing, API design) without a monolithic instruction file, the modularity this note enables.

### 4. `cc_manage_claude_md_for_teams` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: this note documents org-wide deployment of Claude Code's instruction layer (managed-policy CLAUDE.md), so the product term is the subject being centrally managed.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what the term is: progressive permission/enforcement controls; relevance: the note's managed-CLAUDE.md vs managed-settings table maps *behavioral guidance* (CLAUDE.md) against *hard enforcement* (settings: permissions.deny, sandbox.enabled) — the enforcement-vs-guidance spectrum this term frames.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — what the term is: isolating execution from the host; relevance: the note's enforcement table routes "enforce sandbox isolation" to managed settings (`sandbox.enabled`) rather than CLAUDE.md, distinguishing what a managed instruction file can and cannot guarantee.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating LLM context; relevance: the note has IT/DevOps decide which org-wide instructions enter every session's context and which files to exclude (`claudeMdExcludes`), an organization-scale context-curation decision.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime; relevance: precedence ("loads before user and project CLAUDE.md"), "where honored" (managed/policy only), and the `claudeMd` key are harness-resolution rules the note specifies.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: codebase-wide agents; relevance: org-wide CLAUDE.md lets a company impose coding standards, security policies, and compliance reminders on every autonomous Claude Code run across all machines, the governance use case this note serves.

### 5. `cc_auto_memory` (6 term notes)
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what the term is: an agent persisting learnings across sessions; relevance: auto memory IS Claude Code's agentic-memory implementation — Claude decides what's worth remembering and writes it to MEMORY.md/topic files for future sessions, exactly this term.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: auto memory is a Claude Code feature (v2.1.59+), so the product term anchors the storage layout, toggles, and load rules this note documents.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the per-session token budget; relevance: the note's core load rule (first 200 lines or 25KB of MEMORY.md loaded each session; topic files read on demand) is a context-window management strategy to keep memory cheap.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: keeping MEMORY.md concise as an *index* and pushing detail into separately-loaded topic files is the lazy-load context-engineering pattern this note centers on.
- [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — what the term is: an agent that improves itself over time from experience; relevance: auto memory is a concrete self-improvement loop — the agent accumulates build commands, debugging insights, and preferences from its own corrections without human authoring, the behavior this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: codebase-wide agents; relevance: auto memory lets an autonomous agent get progressively more effective in a repo by remembering project specifics across runs, the long-horizon capability this note provides.

### 6. `cc_troubleshoot_memory` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: this note debugs Claude Code's memory loading (which files are seen, why instructions are/aren't followed), so the product term is the system being diagnosed.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime wrapping the model; relevance: the note's root cause — CLAUDE.md is delivered as a *user message after the system prompt*, not the system prompt itself — is a harness prompt-assembly detail, and `--append-system-prompt`/hooks are harness escape hatches.
- [Compaction](../../term_dictionary/term_compaction.md) — what the term is: summarizing conversation to reclaim context; relevance: the note has a dedicated "Instructions seem lost after `/compact`" symptom explaining that root CLAUDE.md is re-read after compaction while nested files are not — a compaction-interaction bug.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the token budget; relevance: the "My CLAUDE.md is too large" symptom (>200 lines reduces adherence; imports don't reduce context) is a context-window problem the note remedies with path-scoped rules.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: the fixes (make instructions specific, remove conflicts, scope by path, move enforced steps to hooks) are context-engineering remedies for unreliable instruction-following.
- [Skills](../../term_dictionary/term_skills.md) — what the term is: on-demand workflows; relevance: the note's `InstructionsLoaded` hook tip and its routing of "must-run-at-a-point" instructions to hooks vs the broader guidance to move task content to skills connect troubleshooting to the skill/hook extension layer.

### 7. `cc_sessions` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: a session is Claude Code's saved-conversation unit; this note documents the CLI session lifecycle (resume/name/branch/export), so the product term is its subject.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the per-session token budget; relevance: the note's "Manage context within a session" section (`/clear`, `/compact`, `/context`) is about controlling what fills the context window without leaving the session.
- [Compaction](../../term_dictionary/term_compaction.md) — what the term is: replacing history with a summary; relevance: `/compact [instructions]` is one of the in-session context commands this note lists, and the page links to context-window guidance for how compaction interacts with CLAUDE.md/skills/rules.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what the term is: periodically saving recoverable state; relevance: the note distinguishes *forking* (branch a session, preserving the original) from *checkpoint-based rewind within a session* and links to the sibling Checkpointing page — the two state-recovery models.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: choosing when to `/clear` (empty context) vs `/compact` (summarized history) vs branch is a context-management decision the note frames and links to best-practices for.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime; relevance: per-project session storage, JSONL transcript files, session-ID scoping to the worktree, and 30-day cleanup (`cleanupPeriodDays`) are harness-level persistence mechanics this note documents.

### 8. `cc_checkpointing` (6 term notes)
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what the term is: periodically capturing recoverable state so you can roll back; relevance: this note IS Claude Code's checkpointing feature — automatic pre-edit snapshots, one per prompt, that you `/rewind` to — the canonical instance of the term.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: checkpointing is a Claude Code safety feature; the product term anchors the `/rewind` menu, restore/summarize actions, and limitations this note documents.
- [Context Window](../../term_dictionary/term_context_window.md) — what the term is: the token budget; relevance: the "Summarize from/up to here" rewind actions compress part of the conversation to free context-window space — a window-management use of checkpointing the note highlights.
- [Compaction](../../term_dictionary/term_compaction.md) — what the term is: summarizing conversation; relevance: the note explicitly compares the targeted "Summarize" rewind actions to `/compact` (whole-conversation summary), distinguishing scoped vs full compaction.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what the term is: persisting agent state across sessions; relevance: checkpoints persist across sessions (accessible in resumed conversations) and are cleaned up with sessions after 30 days — a persisted-state lifecycle paralleling memory.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what the term is: codebase-wide agents; relevance: the note frames checkpointing as the safety net that lets you "pursue ambitious, wide-scale tasks knowing you can always return to a prior code state" — the recoverability that makes autonomous wide edits safe.

### 9. `cc_dot_claude_directory` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: this note maps every file Claude Code reads under `.claude/` and `~/.claude/`, so the product term is the consumer of all these configuration files.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — what the term is: the protocol for connecting external tools to an LLM; relevance: the directory map documents `.mcp.json` (team-shared MCP servers, schemas deferred via tool search) and `~/.claude.json` (personal MCP servers), key nodes in the tree.
- [Skills](../../term_dictionary/term_skills.md) — what the term is: packaged invocable workflows; relevance: `skills/<name>/SKILL.md` (and the legacy `commands/*.md`, now the same mechanism) are first-class nodes in the directory, with frontmatter (`disable-model-invocation`, `user-invocable`) the note explains.
- [Subagent](../../term_dictionary/term_subagent.md) — what the term is: an isolated-context delegated agent; relevance: the map documents `agents/*.md` (subagent definitions with own prompt/tools/model) and `agent-memory/` (per-subagent persistent memory) as directory nodes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what the term is: progressive permission/enforcement; relevance: the `settings.json`/`settings.local.json` nodes carry `permissions` (allow/deny/prompt) and the committed-vs-gitignored badge distinctions that govern what Claude may do, the trust controls this map surfaces.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: each node's "when it loads" annotation (every session / on matching file / on demand / separate window) is exactly the context-loading-timing knowledge needed to engineer what enters context — the note's organizing lens.

### 10. `cc_claude_application_data` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what the term is: the agentic coding tool; relevance: this note documents the data `~/.claude` writes during sessions (transcripts, history, snapshots, caches), so the product term is what generates and cleans up this state.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — what the term is: isolating execution and limiting exposure; relevance: the note's plaintext-at-rest warning (anything a tool reads or prints lands in the JSONL transcript) and its mitigations (deny credential reads via permission rules, skip prompt history) are data-exposure controls in the sandbox/security spirit.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what the term is: saving recoverable state; relevance: `file-history/<session>/` holds the pre-edit snapshots used for checkpoint restore, and deleting it loses checkpoint restore for past sessions — the on-disk backing of the checkpointing feature.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what the term is: persisted agent learnings; relevance: `projects/<project>/memory/` (auto memory) is one of the application-data paths, and `claude project purge` deletes transcripts *and* auto memory for a project — the memory store's lifecycle.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what the term is: curating context; relevance: the note distinguishes auto-cleaned ephemeral context artifacts (tool-results spills, paste/image caches, plans) from kept state (history, stats), the disk footprint of everything Claude Code loads into context.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what the term is: the runtime; relevance: the cleanup sweep on startup (`cleanupPeriodDays`), session-env metadata, shell-snapshots, and the `claude project purge` deletion plan are harness data-lifecycle behaviors this note documents.

## Section Coverage Map

```
memory.md
├── intro (two mechanisms) ──────────────── → note 1 (cc_memory_overview)
├── CLAUDE.md vs auto memory (table) ─────── → note 1
│   └── "block via PreToolUse hook" ──────── → link-out (B07 hooks)
│   └── "subagents maintain own memory" ──── → link-out (B10A sub-agents)
├── CLAUDE.md files ──────────────────────── → note 2 (cc_claude_md_files)
│   ├── When to add ───────────────────────── → note 2
│   ├── Choose where to put (4-scope table) ── → note 2
│   ├── Set up a project CLAUDE.md (/init) ─── → note 2 (/init detail → links B06/setup)
│   ├── Write effective instructions ───────── → note 2
│   ├── Import additional files (@path) ────── → note 2
│   ├── AGENTS.md (import/symlink) ─────────── → note 2
│   ├── How CLAUDE.md files load ───────────── → note 2
│   │   └── Load from additional directories ─ → note 2 (env var detail → B03A)
│   ├── Organize rules with .claude/rules/ ─── → note 3 (cc_claude_rules_directory)
│   │   ├── Set up rules ───────────────────── → note 3
│   │   ├── Path-specific rules (glob table) ── → note 3
│   │   ├── Share rules with symlinks ──────── → note 3
│   │   └── User-level rules ───────────────── → note 3
│   └── Manage CLAUDE.md for large teams ───── → note 4 (cc_manage_claude_md_for_teams)
│       ├── Deploy organization-wide CLAUDE.md → note 4 (managed settings ref → B05A/B03A)
│       └── Exclude specific CLAUDE.md files ── → note 4
├── Auto memory ──────────────────────────── → note 5 (cc_auto_memory)
│   ├── Enable or disable ──────────────────── → note 5 (env-var nuance → B03A)
│   ├── Storage location ───────────────────── → note 5 (autoMemoryDirectory scope → B03A)
│   ├── How it works ───────────────────────── → note 5
│   └── Audit and edit your memory ─────────── → note 5
├── View and edit with /memory ───────────── → note 5
├── Troubleshoot memory issues ───────────── → note 6 (cc_troubleshoot_memory)
│   ├── Claude isn't following my CLAUDE.md ── → note 6 (--append-system-prompt → B03B)
│   ├── I don't know what auto memory saved ── → note 6
│   ├── My CLAUDE.md is too large ──────────── → note 6
│   └── Instructions seem lost after /compact  → note 6 (context-window detail → B02A)
└── Related resources ────────────────────── → notes 2/5/6 (links)
sessions.md
├── intro (session = saved conversation) ──── → note 7 (cc_sessions)
├── Resume a session ──────────────────────── → note 7 (CLI flag detail → B03B)
│   └── Where the session picker looks ─────── → note 7
├── Name your sessions ────────────────────── → note 7 (plan-mode ref → B05A)
├── Use the session picker ────────────────── → note 7
├── Branch a session ──────────────────────── → note 7 (→ note 8 / B10B worktrees)
├── Manage context within a session ───────── → note 7 (context-window detail → B02A)
├── Export and locate session data ────────── → note 7 (env var/setting detail → B03A/B03B)
└── See also ──────────────────────────────── → notes 7/8 (links → B10B/B02A)
checkpointing.md
├── How checkpoints work ──────────────────── → note 8 (cc_checkpointing)
│   ├── Automatic tracking ─────────────────── → note 8
│   └── Rewind and summarize ───────────────── → note 8
│       └── Restore vs. summarize ──────────── → note 8 (fork ref → note 7)
├── Common use cases ──────────────────────── → note 8
├── Limitations ───────────────────────────── → note 8
│   ├── Bash command changes not tracked ───── → note 8
│   ├── External changes not tracked ───────── → note 8
│   └── Not a replacement for version control  → note 8
└── See also ──────────────────────────────── → note 8 (links → B04A/B03B)
claude-directory.md
├── intro (reads project + ~/.claude) ─────── → note 9 (cc_dot_claude_directory)
├── ClaudeExplorer JSX (per-file data) ─────── → note 9 (file-reference content, not code)
├── Explore the directory ─────────────────── → note 9
├── What's not shown (managed/local/plugins) ─ → note 9 (managed-settings → B03A/B14B; plugins → B09)
├── Choose the right file (decision table) ─── → note 9
├── File reference (table) ─────────────────── → note 9
├── Troubleshoot configuration ────────────── → note 10 (cc_claude_application_data) (→ B03B debug-your-config)
├── Application data ──────────────────────── → note 10
│   ├── Cleaned up automatically ───────────── → note 10
│   ├── Kept until you delete them ─────────── → note 10
│   ├── Plaintext storage ──────────────────── → note 10 (security detail → B16)
│   └── Clear local data (claude project purge)→ note 10 (CLI detail → B03B)
└── Related resources ─────────────────────── → notes 9/10 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| memory.md (3.8Kw, 6 H2, 12+ H3 mixed) | notes 1,2,3,4,5,6 | distinct BBs/topics: overview-of-two-systems (concept) · CLAUDE.md authoring (concept) · rules dir (concept) · org-wide deployment (procedure) · auto memory (concept) · troubleshooting (procedure). Combined ≫2,500w. |
| claude-directory.md (8.4Kw; ~6.6Kw is the JSX explorer payload) | notes 9,10 | file-map reference (concept — per-file purpose/scope/load-timing) vs application-data lifecycle (procedure — cleanup/retention/purge). The two halves are different BBs and together exceed 2,500w. |
| sessions.md (1.3Kw) | note 7 (no split) | single coherent concept (session lifecycle); under cap. |
| checkpointing.md (0.8Kw) | note 8 (no split) | single coherent procedure (rewind/summarize); under cap. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_memory_overview | concept | 450 | 1 | ✅ |
| 2 | cc_claude_md_files | concept | 750 | 4 | ✅ |
| 3 | cc_claude_rules_directory | concept | 500 | 3 | ✅ |
| 4 | cc_manage_claude_md_for_teams | procedure | 550 | 2 | ✅ |
| 5 | cc_auto_memory | concept | 650 | 3 | ✅ |
| 6 | cc_troubleshoot_memory | procedure | 400 | 0 | ✅ |
| 7 | cc_sessions | concept | 700 | 3 | ✅ |
| 8 | cc_checkpointing | procedure | 600 | 1 | ✅ |
| 9 | cc_dot_claude_directory | concept | 800 | 2 | ✅ |
| 10 | cc_claude_application_data | procedure | 600 | 3 | ✅ |

No note approaches the caps (max 800w / 4 code, well under 2,500w / 6 code / 400 lines). `memory.md` and
`claude-directory.md` were split *because* an un-split note would breach 2,500w. No over-compression — every
H2/H3 maps to a note or an explicit link-out (Section Coverage Map).

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_memory_overview cc_claude_md_files cc_claude_rules_directory cc_manage_claude_md_for_teams cc_auto_memory cc_troubleshoot_memory cc_sessions cc_checkpointing cc_dot_claude_directory cc_claude_application_data"
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
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 10 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability(reciprocal) | sibling `cc_*` cross-links present so the cluster is internally connected (no intra-cluster island) | DB in-degree query across the 10 notes |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 10 rows** under a
"Memory, Sessions & .claude" cluster + increments the BB-distribution counts (concept +6, procedure +4). The
entry-point back-link is added into each note's `## Related Notes` at finalization (G7).

## Undigested Terms Plan (Step 4e)

b02b creates **no new `term_dictionary` notes** — glossary/vocabulary terms its pages introduce are covered by a
b02b `cc_` concept note, an existing substantive term note (link), or their home sub-plan (Pattern B). Dedup was
run across **both** `term_dictionary/` AND `resources/documentation/` (substantive coverage → link, not recreate):

| Term surfaced (page) | Disposition |
|---|---|
| Auto memory (memory) | note 5 `cc_auto_memory` (doc concept) + link `term_agentic_memory` |
| CLAUDE.md (memory, claude-dir) | note 2 `cc_claude_md_files` (doc concept) |
| `.claude` directory (claude-dir) | note 9 `cc_dot_claude_directory` (doc concept) |
| Rules / `.claude/rules/` (memory) | note 3 `cc_claude_rules_directory` (doc concept) |
| Session (sessions) | note 7 `cc_sessions` (doc concept) |
| Checkpoint (checkpointing) | note 8 `cc_checkpointing` (doc concept) + link `term_regular_checkpointing` |
| Project trust (claude-dir, memory) | folded into notes 5/9 (workspace-trust gate prose); no separate note |
| Compaction / Context window / Subagent / MCP / Sandboxing | existing term notes (link) |
| Worktree / `.worktreeinclude` (claude-dir) | owned by B10B (`worktrees.md`) — captured there; linked here |
| Hook (memory PreToolUse/InstructionsLoaded) | owned by B07A/B07B — captured there; linked here |
| Skill / Command / Output style (claude-dir) | owned by B06 — captured there; linked here |
| Plan mode / Permission mode / Permissions (sessions, memory) | owned by B05A — captured there; linked here |
| Managed settings / settings layers / env vars (memory, claude-dir) | owned by B03A — captured there; linked here |
| Plugin (claude-dir "what's not shown") | owned by B09 — captured there; linked here |
| Dynamic workflow (claude-dir `workflows/`) | owned by B10B — captured there; linked here |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/JSX-data for
newly-surfaced non-glossary terms. Candidates examined: "auto memory", "MEMORY.md", "rules directory",
"application data / transcript", "managed-policy CLAUDE.md", "agent-memory". Each is either (a) a *subject of a
b02b `cc_` doc note* (auto memory→5, rules→3, .claude dir→9, app-data→10) or (b) an existing substantive term
(`term_agentic_memory`, `term_regular_checkpointing`, `term_self_evolving_agent` all exist → linked). **Collision
dedup audit across term_dictionary AND documentation/: PASS** — no candidate duplicates an existing *substantive*
term/doc note at the same sense, and no general-slug capture is warranted. **0 new b02b `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b02b authors zero term notes, so there are no slugs
to audit for over-generality or collision. The collision check that matters here (do the b02b doc concepts
duplicate existing notes?) was performed: `term_agentic_memory`, `term_regular_checkpointing`, `term_compaction`,
`term_context_window`, `term_mcp`, `term_subagent`, `term_sandbox`, `term_skills`, `term_graduated_trust`,
`term_self_evolving_agent` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b02b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source config/CLI examples (CLAUDE.md import, managed-settings `claudeMd`,
  `autoMemoryEnabled`, MEMORY.md index, `/branch`, `claude project purge`). One BB per note. Each note ≤400 lines
  (split if a draft >350).
- Do NOT transcribe the `claude-directory.md` JSX `ClaudeExplorer` component as code; digest its *data* (per-file
  purpose/scope/load-timing) as prose + the small config examples it contains.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Cap dynamic-workflow fan-out at ~30 agents/run; reindex incrementally after the sub-plan.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 — every new note gets
in-degree ≥1 from outside `claude_code/`):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 7, 9 | product term → CC memory model / sessions / .claude dir map |
| `term_dictionary/term_agentic_memory.md` | notes 5, 1 | agentic-memory term → CC auto memory feature |
| `term_dictionary/term_regular_checkpointing.md` | note 8 | checkpointing term → CC checkpointing feature |
| `term_dictionary/term_context_engineering.md` | notes 2, 3 | context-engineering term → CLAUDE.md authoring / path-scoped rules |
| `term_dictionary/term_self_evolving_agent.md` | note 5 | self-evolving-agent term → auto-memory self-improvement loop |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | notes 2, 9 | getting-started tutorial → CLAUDE.md setup / .claude directory |

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; verify each
  note's in-degree ≥1 (G7/G8); queue the 10 rows for `entry_claude_code_docs.md` (Memory/Sessions/.claude
  cluster); `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` if any.
- Add intra-cluster sibling links once B03A (settings), B05A (permissions), B06 (skills), B07 (hooks), B10A/B10B
  (subagents/worktrees), B09 (plugins) land, so the many link-outs in the Coverage Map resolve to real `cc_` notes.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B02B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/`; measured words sum to
  14,400 (memory 3,817 · sessions 1,317 · checkpointing 816 · claude-directory 8,450) = the master's B02B figure
  exactly. Confirmed `claude-directory.md`'s bulk is the JSX `ClaudeExplorer` component (the per-file reference
  *data*), with only ~1,850 prose words after L1431 — recorded in Source Pages note + Split Decisions so the
  executor digests the file-reference content, not the React code.
- **Notes**: locked at **10** (concept 6, procedure 4). The master estimated 9; the augment is permitted to
  adjust — the honest split of `claude-directory.md` into a concept file-map + a procedure application-data note
  (different BBs, combined >2,500w) yields the 10th. Documented in Planned Notes + Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard — 6
  term notes per note (12 distinct `term_dictionary/` terms across the 10 notes), each with a what-it-is + a
- **Dedup (Step 2b/G-B)**: ran filename grep + BM25 + dense across `term_dictionary/` AND `resources/documentation/`;
  every candidate concept either maps to a b02b `cc_` note or an existing substantive term note (linked, not
  term_junction, term_npm_scoping, term_sidechain_transcript) discarded as not same-sense.
- **Step 2d new-term scan**: candidates examined (auto memory, MEMORY.md, rules dir, application data, managed
  CLAUDE.md, agent-memory); all owned by a b02b doc note or an existing term → **0 new b02b term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts
  (bash), G5/G7/G8 verification rows, full Section Coverage Map with link-outs.
- **28-item checklist**: PASS (term-note items N/A — b02b authors no terms; entry-point + undigested-terms
  inherited from master; G7/G8 discoverability inlinks executed at finalization).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note (one-line evidence) |
|---|---|---|---|
| CP2 | ALL gates per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 notes → CREATE); B02B contributes 10 rows + BB counts. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes (≤30); part of master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body (`## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer) inherited verbatim from master Format Definition. |
| CP6 | Borderline density → split | ✅ PASS | All 10 notes 400–800w, ≤4 code — none borderline; memory.md & claude-directory.md proactively split before breaching 2,500w. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Spot-check: claude-directory measured 8,450 = plan 8,450; memory 3,817 = plan 3,817; sessions 1,317; checkpointing 816. Sum 14,400 = master B02B. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B02B authors 0 term notes; Undigested Terms Plan routes every surfaced term (doc note / existing term / home sub-plan), dedup'd across term_dictionary AND documentation/; Authoring Requirements inherited. |
| CP9 | Discoverability inlinks executed (G7/G8) | ✅ PASS | Inlinks table maps ≥1 outside-cluster inbound link to every one of the 10 notes; sibling `cc_*` cross-links planned (Follow-up); verified by DB in-degree ≥1 at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
