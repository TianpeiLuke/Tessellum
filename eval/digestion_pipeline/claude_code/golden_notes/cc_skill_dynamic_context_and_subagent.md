---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - advanced_patterns
keywords:
  - dynamic context injection
  - shell command preprocessing
  - context fork
  - subagent execution
  - pre-approve tools
  - allowed-tools
  - disableSkillShellExecution
  - visual output skill
topics:
  - Claude Code
  - Skills
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/skills
access_control_group: ["general"]
---

# Claude Code Skills — Dynamic Context, Subagent Execution & Tool Pre-Approval

## Overview

Beyond a plain instruction body, a Claude Code skill can be wired with three advanced patterns documented here: **dynamic context injection** (running shell commands and inlining their output before Claude reads the skill), **subagent execution** (`context: fork` runs the skill body as the prompt for an isolated subagent), and **tool pre-approval** (`allowed-tools` grants permission for listed tools while the skill is active). A fourth pattern bundles and runs scripts to produce **visual output** (e.g. interactive HTML), letting a skill do work beyond a single prompt.

This procedure note shows how to apply each pattern: the `` !`command` `` inline and ` ```! ` fenced injection syntax (with its single-pass, line-start, and policy-disable rules), the `context: fork` + `agent:` forked-execution flow, the `allowed-tools`/`disallowed-tools` pre-approval mechanism, and the bundled-script-plus-`${CLAUDE_SKILL_DIR}` visual-output pattern.

## Inject dynamic context

The `` !`<command>` `` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.

This skill summarizes a pull request by fetching live PR data with the GitHub CLI. The `` !`gh pr diff` `` and other commands run first, and their output gets inserted into the prompt:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

When this skill runs:

1. Each `` !`<command>` `` executes immediately (before Claude sees anything).
2. The output replaces the placeholder in the skill content.
3. Claude receives the fully-rendered prompt with actual PR data.

This is **preprocessing, not something Claude executes** — Claude only sees the final result. Substitution runs **once over the original file**: command output is inserted as plain text and is not re-scanned for further `` !`<command>` `` placeholders, so a command cannot emit a placeholder for a later pass to expand.

**Line-start rule.** The inline form is only recognized when `!` appears at the start of a line or immediately after whitespace. If `!` follows another character — as in `` KEY=!`cmd` `` — the placeholder is left as literal text and the command does not run.

**Multi-line commands.** For multi-line commands, use a fenced code block opened with ` ```! ` instead of the inline form:

````markdown
## Environment
```!
node --version npm --version git status --short
```
````

**Disabling it by policy.** To disable this behavior for skills and custom commands from user, project, plugin, or additional-directory sources, set `"disableSkillShellExecution": true` in settings. Each command is then replaced with `[shell command execution disabled by policy]` instead of being run. Bundled and managed skills are not affected. This setting is most useful in managed settings, where users cannot override it.

> **Tip (verbatim):** To request deeper reasoning when a skill runs, include `ultrathink` anywhere in the skill content.

## Run skills in a subagent

Add `context: fork` to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won't have access to your conversation history.

> **Warning (verbatim):** `context: fork` only makes sense for skills with explicit instructions. If your skill contains guidelines like "use these API conventions" without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output.

Skills and subagents work together in two directions:

| Approach | System prompt | Task | Also loads |
| :--- | :--- | :--- | :--- |
| Skill with `context: fork` | From agent type | SKILL.md content | CLAUDE.md, except when the agent is Explore or Plan |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

With `context: fork`, you write the task in your skill and pick an agent type to execute it. The built-in Explore and Plan agents skip CLAUDE.md and git status to keep their context small, so a forked skill using `agent: Explore` sees only the SKILL.md content and the agent's own system prompt. For the inverse — defining a custom subagent that uses skills as reference material — see [Subagents](https://code.claude.com/docs/en/sub-agents).

**Example: research skill using the Explore agent.** This skill runs research in a forked Explore agent. The skill content becomes the task, and the agent provides read-only tools optimized for codebase exploration:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

When this skill runs: (1) a new isolated context is created; (2) the subagent receives the skill content as its prompt ("Research $ARGUMENTS thoroughly..."); (3) the `agent` field determines the execution environment (model, tools, and permissions); (4) results are summarized and returned to your main conversation. The `agent` field specifies which subagent configuration to use — built-in agents (`Explore`, `Plan`, `general-purpose`) or any custom subagent from `.claude/agents/`. If omitted, it uses `general-purpose`.

## Pre-approve tools for a skill

The `allowed-tools` field grants permission for the listed tools while the skill is active, so Claude can use them without prompting you for approval. It does **not** restrict which tools are available: every tool remains callable, and your permission settings still govern tools that are not listed.

For skills checked into a project's `.claude/skills/` directory, `allowed-tools` takes effect after you accept the workspace trust dialog for that folder, the same as permission rules in `.claude/settings.json`. Review project skills before trusting a repository, since a skill can grant itself broad tool access.

This skill lets Claude run git commands without per-use approval whenever you invoke it:

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

To **remove** tools from Claude's available pool while a skill is active, list them in `disallowed-tools` in the skill's frontmatter. The restriction clears when you send your next message. To block tools across all skills and prompts, add deny rules in your permission settings.

## Generate visual output

Skills can bundle and run scripts in any language, giving Claude capabilities beyond what's possible in a single prompt. One powerful pattern is generating visual output: interactive HTML files that open in your browser for exploring data, debugging, or creating reports. The example in the source is a codebase explorer — an interactive tree view where you can expand and collapse directories, see file sizes at a glance, and identify file types by color.

Create the skill directory:

```bash
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

The `SKILL.md` description tells Claude when to activate the skill, and the instructions tell Claude to run the bundled script. The script path uses `${CLAUDE_SKILL_DIR}` so it resolves correctly whether the skill is installed at the personal, project, or plugin level — for example `python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .`. The frontmatter pre-approves the runner with `allowed-tools: Bash(python3 *)`, which creates `codebase-map.html` in the current directory and opens it in the default browser.

The bundled `scripts/visualize.py` (summarized here, not transcribed) scans a directory tree and generates a **self-contained HTML file** with: a summary sidebar (file count, directory count, total size, number of file types); a bar chart breaking down the codebase by file type (top 8 by size); and a collapsible tree with color-coded file-type indicators. The script requires Python 3 but uses only built-in libraries, so there are no packages to install. To test, open Claude Code in any project and ask "Visualize this codebase." — Claude runs the script, generates `codebase-map.html`, and opens it in your browser.

This pattern works for any visual output — dependency graphs, test coverage reports, API documentation, or database schema visualizations: the bundled script does the work while Claude handles orchestration.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
