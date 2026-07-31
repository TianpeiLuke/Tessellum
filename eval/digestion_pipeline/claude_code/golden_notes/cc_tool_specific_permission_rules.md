---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - rule_syntax
keywords:
  - tool-specific permission rules
  - bash wildcard matching
  - compound commands
  - process wrappers
  - read-only commands
  - powershell ast
  - read and edit gitignore anchors
  - webfetch domain
  - mcp tool rules
  - agent subagent rules
  - cd allowlist
topics:
  - Claude Code
  - Permissions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/permissions
access_control_group: ["general"]
---

# Claude Code — Tool-Specific Permission Rules

## Overview

Beyond the generic `Tool` / `Tool(specifier)` rule syntax, each Claude Code tool interprets its specifier with its own dialect. This note catalogs those per-tool rule grammars: Bash wildcard/word-boundary matching plus its compound-command splitting, process-wrapper stripping, and built-in read-only command set; the PowerShell AST-based variant; the gitignore-anchored `Read`/`Edit` patterns and symlink handling; the `WebFetch(domain:...)` hostname matcher; the `mcp__server__tool` MCP form; the `Agent(AgentName)` subagent control; and the `Cd` allowlist for the `/cd` command.

Across every dialect the deny-first precedence holds: deny rules still run before ask and allow rules regardless of specificity, so these per-tool grammars only refine *what* a rule matches, not the order in which matches are resolved.

## Bash

Bash permission rules support wildcard matching with `*`, and wildcards can appear at any position in the command — beginning, middle, or end:

- `Bash(npm run build)` matches the exact Bash command `npm run build`
- `Bash(npm run test *)` matches Bash commands starting with `npm run test`
- `Bash(npm *)` matches any command starting with `npm `
- `Bash(* install)` matches any command ending with ` install`
- `Bash(git * main)` matches commands like `git checkout main` and `git log --oneline main`

A single `*` matches any sequence of characters including spaces, so one wildcard can span multiple arguments: `Bash(git *)` matches `git log --oneline --all`, and `Bash(git * main)` matches `git push origin main` as well as `git merge main`.

When `*` appears at the end with a space before it (like `Bash(ls *)`), it enforces a **word boundary**, requiring the prefix to be followed by a space or end-of-string. So `Bash(ls *)` matches `ls -la` but not `lsof`. In contrast, `Bash(ls*)` without a space matches both because there is no word-boundary constraint.

> Bash patterns that try to constrain command arguments are fragile (option-before-URL, protocol swaps, redirects, variables, extra spaces all defeat a rule like `Bash(curl http://github.com/ *)`). For reliable URL filtering the docs recommend denying `curl`/`wget` and using `WebFetch(domain:...)`, or a PreToolUse hook; `CLAUDE.md` guidance shapes behavior but does not enforce a boundary. Using WebFetch alone does not prevent network access if Bash is allowed.

### Compound commands

Claude Code is aware of shell operators, so a rule like `Bash(safe-cmd *)` will **not** give permission to run `safe-cmd && other-cmd`. The recognized command separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines. A rule must match each subcommand independently.

When you approve a compound command with "Yes, don't ask again", Claude Code saves a separate rule for **each** subcommand that requires approval rather than one rule for the full string. Approving `git status && npm test` saves a rule for `npm test`, so future `npm test` invocations are recognized regardless of what precedes the `&&`. Subcommands like `cd` into a subdirectory generate their own Read rule for that path. Up to **5 rules** may be saved for a single compound command.

### Process wrappers

Before matching Bash rules, Claude Code strips a fixed set of process wrappers so a rule like `Bash(npm test *)` also matches `timeout 30 npm test`. The recognized wrappers are `timeout`, `time`, `nice`, `nohup`, and `stdbuf`. Bare `xargs` is also stripped (so `Bash(grep *)` matches `xargs grep pattern`), but only when `xargs` has no flags — `xargs -n1 grep pattern` is matched as an `xargs` command, so inner-command rules do not cover it.

This list is **built in and not configurable**. Development-environment runners such as `direnv exec`, `devbox run`, `mise exec`, `npx`, and `docker exec` are **not** in the list. Because they execute their arguments as a command, `Bash(devbox run *)` matches whatever comes after `run`, including `devbox run rm -rf .`. To approve work inside a runner, write a specific rule that includes both the runner and the inner command, such as `Bash(devbox run npm test)`, one rule per inner command.

Exec wrappers such as `watch`, `setsid`, `ionice`, and `flock` always prompt and cannot be auto-approved by a prefix rule like `Bash(watch *)`. The same applies to `find` with `-exec` or `-delete`: a `Bash(find *)` rule does not cover those forms — write an exact-match rule for the full command string.

### Read-only commands

Claude Code recognizes a built-in set of Bash commands as read-only and runs them without a permission prompt in every mode: `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`, and read-only forms of `git`. The set is not configurable; to require a prompt for one, add an `ask` or `deny` rule.

Unquoted glob patterns are permitted for commands whose every flag is read-only, so `ls *.ts` and `wc -l src/*.py` run without a prompt. Commands with write- or exec-capable flags (`find`, `sort`, `sed`, `git`) still prompt when an unquoted glob is present, because the glob could expand to a flag like `-delete`. A `cd` into a path inside your working directory or an additional directory is also read-only, and `cd packages/api && ls` runs without a prompt when each part qualifies on its own — but combining `cd` with `git` in one compound command always prompts, regardless of the target directory.

## PowerShell

PowerShell rules use the same shape as Bash rules: wildcards with `*` match at any position, the `:*` suffix is equivalent to a trailing ` *`, and a bare `PowerShell` or `PowerShell(*)` matches every command. Common aliases are canonicalized before matching, so a rule written for the cmdlet name also matches its aliases — `PowerShell(Get-ChildItem *)` matches `gci`, `ls`, and `dir`. Matching is case-insensitive. Claude Code parses the PowerShell AST and checks each command in a compound command independently: pipeline operators `|`, statement separators `;`, and (on PowerShell 7+) the chain operators `&&` and `||` split a compound command into subcommands, and a rule must match every subcommand.

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

## Read and Edit

`Edit` rules apply to all built-in tools that edit files. Claude makes a best-effort attempt to apply `Read` rules to all built-in file-reading tools like Grep and Glob, to `@file` mentions in prompts, and to the selection and open-file context a connected IDE shares. Read and Edit **deny** rules also apply to file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`), but **not** to arbitrary subprocesses that read or write files indirectly (e.g. a Python or Node script). For OS-level enforcement that blocks all processes, enable the [sandbox](https://code.claude.com/docs/en/sandboxing).

Read and Edit rules both follow the gitignore specification with four anchor types:

| Pattern | Meaning | Example | Matches |
| --- | --- | --- | --- |
| `//path` | **Absolute** path from filesystem root | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**` |
| `~/path` | Path from **home** directory | `Read(~/Documents/*.pdf)` | `/Users/alice/Documents/*.pdf` |
| `/path` | Path **relative to project root** | `Edit(/src/**/*.ts)` | `<project root>/src/**/*.ts` |
| `path` or `./path` | Path **relative to current directory** | `Read(*.env)` | `<cwd>/*.env` |

A pattern like `/Users/alice/file` is **NOT** absolute — it is relative to the project root; use `//Users/alice/file` for absolute paths. On Windows, paths are normalized to POSIX form before matching (`C:\Users\alice` becomes `/c/Users/alice`, so use `//c/**/.env` for a drive and `//**/.env` across all drives). A rule only matches files under its anchor, so the anchor determines how far a deny rule reaches; bare filenames follow gitignore semantics and match at any depth, so `Read(.env)` and `Read(**/.env)` are equivalent. In gitignore patterns `*` matches within a single path segment while `**` matches across directories; to allow all file access use the bare tool name (`Read`, `Edit`, or `Write`).

When Claude accesses a **symlink**, permission rules check two paths — the symlink itself and the file it resolves to — and allow and deny rules treat the pair differently:

- **Allow rules** apply only when **both** the symlink path and its target match; a symlink inside an allowed directory that points outside it still prompts.
- **Deny rules** apply when **either** the symlink path or its target matches; a symlink that points to a denied file is itself denied.

For example, with `Read(./project/**)` allowed and `Read(~/.ssh/**)` denied, a symlink at `./project/key` pointing to `~/.ssh/id_rsa` is blocked: the target fails the allow rule and matches the deny rule.

## WebFetch

WebFetch rules use a `domain:` prefix and match against the hostname of the requested URL. Matching is case-insensitive, supports `*` wildcards, and strips a trailing `.` from both the rule and the hostname (`example.com.` and `example.com` are treated the same):

- `WebFetch(domain:example.com)` matches requests to `example.com`
- `WebFetch(domain:*.example.com)` matches any subdomain at any depth (`api.example.com`, `a.b.example.com`) but **not** `example.com` itself
- `WebFetch(domain:*)` matches every domain and is equivalent to a bare `WebFetch` rule

A `*` matches across a `.` only as a leading `*.` or as the entire pattern; elsewhere it stays within one label, so `WebFetch(domain:github.*)` matches `github.io` but not `github.evil.com` (a domain an attacker could register). When an exact rule and a wildcard rule in the same list both match a hostname, the **exact** rule is matched. Evaluation order is unchanged: deny rules still run before ask and allow rules regardless of specificity.

## MCP

- `mcp__puppeteer` matches any tool provided by the `puppeteer` server (name configured in Claude Code)
- `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server
- `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool provided by the `puppeteer` server

## Agent (subagents)

Use `Agent(AgentName)` rules to control which subagents Claude can use: `Agent(Explore)` matches the Explore subagent, `Agent(Plan)` matches the Plan subagent, and `Agent(my-custom-agent)` matches a custom subagent named `my-custom-agent`. Add these rules to the `deny` array in your settings or use the `--disallowedTools` CLI flag to disable specific agents. To disable the Explore agent:

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Cd

`Cd` rules control which directories the `/cd` command can move the session to. `Cd` is **not** a model-invocable tool: Claude cannot call it, and the rules apply only when you run `/cd` yourself. A bare `Cd` deny rule disables `/cd` entirely, and a `Cd(<path-pattern>)` deny rule blocks matching targets. Deny rules check every spelling of the target, including each symlink hop it resolves through, so a rule written for one path also blocks targets that resolve to it.

Adding any `Cd` allow rule switches `/cd` to **allowlist mode**: the resolved target directory must match one of your allow rules, or `/cd` refuses. With no `Cd` rules configured, `/cd` keeps its default behavior and prompts you to trust an unfamiliar directory. Path patterns share the `//`, `~/`, and `/` anchors from Read and Edit rules, but matching is anchored to the whole directory path rather than gitignore-style: `*` matches exactly one path segment and `**` matches across segments, and a trailing `/**` also matches its named root.

| Rule | Matches | Does not match |
| --- | --- | --- |
| `Cd(~/code/*)` | `~/code/app` | `~/code/app/src`, `~/code` |
| `Cd(~/code/**)` | `~/code` and any directory under it | directories outside `~/code` |
| `Cd(**/node_modules)` | any `node_modules` directory at any depth | `node_modules/pkg` |

**Source**: https://code.claude.com/docs/en/permissions
**Last Updated**: 2026-06-13
**Status**: Active
