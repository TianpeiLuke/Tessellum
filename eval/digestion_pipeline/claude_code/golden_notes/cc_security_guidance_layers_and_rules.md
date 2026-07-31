---
tags:
  - resource
  - documentation
  - claude_code
  - security
  - security_guidance
keywords:
  - security guidance plugin layers
  - per-edit pattern check
  - end-of-turn diff review
  - commit and push review
  - review independence
  - security-patterns.yaml
  - claude-security-guidance.md
  - defense in depth
  - hook integration
topics:
  - Claude Code
  - Security
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/security-guidance
access_control_group: ["general"]
---

# Security Guidance Plugin — Review Layers and Custom Rules

## Overview

The security-guidance plugin reviews Claude's own code changes at **three points, each at a different depth**: a fast per-edit pattern match with no model call, a background end-of-turn diff review, and a deeper agentic review on every commit or push Claude makes. The reviews run as a **separate Claude instance** with fresh context and a security-focused prompt, so Claude is not asked to grade its own work; none of the layers block writes or commits, so the plugin is one layer of defense in depth rather than a complete security solution.

You extend the layers through two additive **extension points** — a Markdown guidance file for the model-backed reviews and a YAML/JSON patterns file for the per-edit string match — and the whole plugin is built on Claude Code **hooks** that register on the agent's lifecycle events. This note covers what each layer checks, the custom-rule schema, usage cost, hook integration, how the plugin fits with other security tools, and troubleshooting. For installing, enabling in cloud/shared repositories, and disabling/uninstalling, see [Security Guidance Plugin — Install and Enable](cc_security_guidance_plugin.md).

## What the Plugin Checks

The plugin reviews Claude's work at three points, each at a different depth:

- **On each file edit**: a fast pattern match for risky calls, with no model call
- **At the end of each turn**: a background model review of everything that turn changed
- **On each commit or push Claude makes**: a deeper agentic review that reads surrounding code

You can extend each layer by adding your own rules. Built-in checks cannot be removed individually, but you can disable each layer independently (see [Install and Enable](cc_security_guidance_plugin.md)).

### On each file edit

When Claude writes to a file, the plugin scans the new content for known risky patterns. This is a pattern match with no model call, so it adds no usage cost. Example pattern categories:

- **Dynamic code execution**: `eval(`, `new Function`, `os.system`, `child_process.exec`
- **Unsafe deserialization**: `pickle`
- **DOM injection**: `dangerouslySetInnerHTML`, `.innerHTML =`, `document.write`
- **Workflow files**: edits under `.github/workflows/`, which can grant repository-level permissions

The check runs after the edit lands and appends the warning to Claude's context for the next step. Each warning fires once per pattern per file per session, so repeat matches in the same file do not flood the conversation. You can add your own patterns to this layer with a `security-patterns.yaml` file (see below).

### At the end of each turn

A turn is one round of Claude responding: you send a message, Claude works and replies, and the turn ends. After each turn, the plugin computes a git diff of everything that changed in the working tree during the turn — including changes from Claude's edit tools, Bash commands, and subagents — and sends it to a separate Claude review focused on security. The review runs in the background, so Claude's reply is not delayed. If the review finds issues, Claude is re-prompted with the findings and addresses them as a follow-up. This catches issues a string match cannot, such as:

- Authorization bypass
- Insecure direct object references
- Injection
- Server-side request forgery
- Weak cryptography

You see both the finding and Claude's resolution directly in your session. The review covers up to **30 changed files per turn** and fires **at most three times in a row** before yielding back to you.

### On each commit or push Claude makes

When Claude runs `git commit` or `git push` through its Bash tool, the plugin runs a deeper agentic review of the change in the background. This review reads surrounding code — including callers, sanitizers, and related files — to decide whether a finding is real before reporting it. The extra context keeps false positives low on patterns that look dangerous in isolation but are safe in your codebase.

This layer fires only on commits and pushes Claude makes through its Bash tool. Commits you run from your own shell, including the `!` shell escape inside a session, are not reviewed. Commit and push reviews are capped at **20 per rolling hour**. If the commit review's findings duplicate what the end-of-turn review already reported, Claude is not re-prompted, so a clean commit produces no visible output from this layer.

### Review independence and limits

The plugin does not ask the same Claude instance that wrote the code to grade itself. The per-edit check is a deterministic string match with no model involved. The end-of-turn and commit reviews run as a separate Claude call with a fresh context and a security-focused prompt: the reviewer starts from the diff, has no investment in the original approach, and is instructed only to find problems.

None of the layers block writes or commits. Findings reach the writing Claude as instructions, Claude addresses them in the conversation, and the review model can miss issues. Treat the plugin as one layer of defense in depth, not a complete security solution.

## Add Your Own Rules

The plugin has two extension points: a Markdown guidance file for the model-backed reviews, and a YAML or JSON patterns file for the per-edit string match. Both are additive — you can add checks but cannot disable built-in ones from these files.

### Add guidance for the model-backed reviews

Create `.claude/claude-security-guidance.md` in your project and describe your threat model and review checklist in plain language. The model-backed reviews load it as additional context alongside the built-in vulnerability checklist. The following example is for a web service with role-gated admin routes and a customer-data logging policy:

```markdown .claude/claude-security-guidance.md theme={null}
# Security guidance for this repo

- Do not log `customer_id` or `account_number` at INFO level or above.
- All routes under `/admin` must call `require_role("admin")` before any database read.
- Use `crypto.timingSafeEqual` for token comparison instead of `===`.
```

These rules are guidance for the reviewer, not deterministic guardrails. The plugin surfaces violations as findings for Claude to fix, but it does not block writes or guarantee every violation is caught. The guidance is additive only: a rule that says to ignore a vulnerability class does not suppress those findings. For hard enforcement, pair the plugin with a hook that blocks the edit or a CI check.

### Add custom per-edit patterns

Create `.claude/security-patterns.yaml` to add regex or substring rules to the per-edit pattern check. These run as deterministic string matches alongside the built-in patterns:

```yaml .claude/security-patterns.yaml theme={null}
patterns:
  - rule_name: internal_api_key
    substrings: ["sk_live_", "AKIA"]
    reminder: "Hardcoded API key prefix. Load credentials from the secret manager."
  - rule_name: tenant_unfiltered_query
    regex: "\\.objects\\.all\\(\\)"
    paths: ["**/src/tenants/**"]
    reminder: "Multi-tenant code must filter by org_id."
```

The pattern fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `rule_name` | string | Identifier shown in the warning |
| `reminder` | string | Warning text appended to Claude's context, capped at 1 KB |
| `regex` | string | Python regex matched against the edited content |
| `substrings` | list | Literal substrings; provide this or `regex` |
| `paths` | list | Optional glob patterns; the rule applies only to matching files. Globs match against the full file path, so prefix project-relative patterns with `**/` |
| `exclude_paths` | list | Optional glob patterns to skip; same matching as `paths` |

The plugin also reads `.claude/security-patterns.yml` and `.claude/security-patterns.json` with the same schema. JSON works on any Python install. The YAML forms require PyYAML to be importable, which the plugin does not install for you. The plugin loads up to **50 custom rules** and skips regexes that look prone to catastrophic backtracking.

### Rule file lookup locations

The plugin looks for `claude-security-guidance.md` and `security-patterns.yaml` in the same locations, independently of how the plugin was enabled:

| Scope | Path | Notes |
| :--- | :--- | :--- |
| User | `~/.claude/claude-security-guidance.md` | Applies to every project on your machine |
| Project | `.claude/claude-security-guidance.md` | Checked in with the repository |
| Project local | `.claude/claude-security-guidance.local.md` | Gitignored, for personal overrides |

The plugin loads all locations that exist and concatenates them, with a combined cap of **8 KB** for the guidance file. Administrators can distribute organization-wide rules by pushing the user-scope file to `~/.claude/` through device management. The same paths apply to `security-patterns.yaml`.

## Usage Cost

The per-edit pattern check makes no model call and adds no cost. The end-of-turn and commit reviews each spend additional model usage that counts toward your usage like any other Claude request. The commit review is agentic and may take several model turns per commit, capped at 20 reviews per rolling hour. Expect roughly one review call per turn that changes files and one deeper review per commit, both subject to the caps above.

Both model-backed reviews use **Claude Opus 4.7** by default. Set `SECURITY_REVIEW_MODEL` to choose a different model for the end-of-turn review and `SG_AGENTIC_MODEL` for the commit review. The plugin is available on all plans.

## How the Plugin Integrates with Claude Code

The plugin is built entirely on hooks, the mechanism for running your own code at specific points in Claude's loop. It registers:

| Hook event | Purpose |
| :--- | :--- |
| `SessionStart` | Bootstrap the plugin's Python environment |
| `UserPromptSubmit` | Capture the working-tree baseline that the end-of-turn review diffs against |
| `PostToolUse` on `Edit`, `Write`, and `NotebookEdit` | Per-edit pattern match |
| `Stop` | End-of-turn diff review, run in the background |
| `PostToolUse` on `Bash`, filtered to `git commit` and `git push` | Commit and push review, run in the background |

If you build your own hooks, the plugin's source (`github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance`) is a working example of running a separate model call from a hook and feeding the result back to the session. For the hook-event registry and how hooks run in Claude's loop, see the [hooks reference](https://code.claude.com/docs/en/hooks).

## How This Fits with Other Security Tools

The plugin is one layer in a defense-in-depth approach. It catches issues earliest, while code is still in the editor, but it is not a guarantee and does not replace later checks. A typical stack:

| Stage | Tool | What it covers |
| :--- | :--- | :--- |
| In session | Security guidance plugin | Common vulnerabilities in code Claude writes, fixed in the same session |
| On demand | `/security-review` | One-time security pass on the current branch, run when you ask |
| On pull request | Code Review (Team and Enterprise plans) | Multi-agent correctness and security review with full codebase context |
| In CI | Your existing static analysis and dependency scanners | Language-specific rules, supply-chain checks, and policy enforcement the plugin does not attempt |

Each later stage catches what earlier ones miss. The plugin's value is reducing the volume that reaches them, not eliminating the need for them. (For the `/security-review` command see the [commands reference](https://code.claude.com/docs/en/commands); for PR-time review see [Code Review](https://code.claude.com/docs/en/code-review).)

## Troubleshooting

The plugin writes runtime diagnostics to `~/.claude/security/log.txt`. Check there first if reviews are not appearing. Common reasons a review layer skips without a message in the conversation:

- **The directory is not a git repository**: the end-of-turn and commit reviews require git state and skip outside a repository
- **The session has no Anthropic authentication**: the model-backed reviews skip and only the per-edit pattern check runs
- **A `security-patterns.yaml` file is present but PyYAML is not importable**: the file is ignored. Use `security-patterns.json` instead

**Source**: https://code.claude.com/docs/en/security-guidance
**Last Updated**: 2026-06-13
**Status**: Active
