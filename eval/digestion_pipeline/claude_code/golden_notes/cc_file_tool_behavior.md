---
tags:
  - resource
  - documentation
  - claude_code
  - tools
  - file_tools
keywords:
  - read tool paging
  - edit read-before-edit
  - exact string replacement
  - write overwrite rule
  - notebookedit cell modes
  - glob pattern matching
  - grep ripgrep regex
  - gitignore behavior
topics:
  - Claude Code
  - Tools
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/tools-reference
access_control_group: ["general"]
---

# Claude Code — File and Search Tool Behavior

## Overview

This note documents the per-tool semantics of Claude Code's six built-in **file and search tools** — `Read`, `Edit`, `Write`, `NotebookEdit`, `Glob`, and `Grep`. These are the tools Claude uses to inspect, modify, and locate files in a codebase. Their precise behaviors — read-before-edit gating, exact-string matching, token-limit paging, `.gitignore` handling, and ripgrep regex — are what let an agent edit safely and search efficiently. For the full tool catalog and the shared `ToolName(specifier)` permission-rule format, see [cc_tools_catalog.md](cc_tools_catalog.md); for the execution and web tools (`Bash`, `Agent`, `WebFetch`, etc.) see [cc_execution_tool_behavior.md](cc_execution_tool_behavior.md).

These tools split by permission: `Edit`, `Write`, and `NotebookEdit` require permission; `Read`, `Glob`, and `Grep` do not. To disable any tool entirely, add its name to the `deny` array in [permission settings](https://code.claude.com/docs/en/permissions).

## Read tool behavior

The Read tool takes a file path and returns the contents with line numbers. Claude is instructed to always pass absolute paths.

By default, Read returns the file from the start. When a whole-file read exceeds the token limit, Read returns the first page with a `PARTIAL view` notice that tells Claude how much of the file it received and how to read more with `offset` and `limit`. A read that passes an explicit `offset` or `limit` and still exceeds the token limit returns an error.

Read handles several file types beyond plain text:

- **Images**: PNG, JPG, and other image formats are returned as visual content that Claude can see, not as raw bytes. Claude Code resizes and recompresses large images to fit the model's image size limits before sending them, so Claude may see a downscaled version of a large screenshot. If Claude misses fine pixel-level detail in a large image, ask it to crop the region of interest first, for example with ImageMagick via Bash.
- **PDFs**: Claude reads short `.pdf` files whole. For PDFs longer than 10 pages, it reads in ranges with a `pages` parameter, such as `"1-5"`, up to 20 pages at a time.
- **Jupyter notebooks**: `.ipynb` files return all cells with their outputs, including code, markdown, and visualizations.

Read only reads files, not directories. Claude uses `ls` via the Bash tool to list directory contents.

## Edit tool behavior

The Edit tool performs **exact string replacement**. It takes an `old_string` and a `new_string` and replaces the first with the second. It does not use regex or fuzzy matching.

Three checks must pass for an edit to apply:

- **Read-before-edit**: Claude must have read the file in the current conversation, and the file must not have changed on disk since that read. This check runs first, before any string matching.
- **Match**: `old_string` must appear in the file exactly as written. A single character of whitespace or indentation difference is enough to miss.
- **Uniqueness**: `old_string` must appear exactly once. When it appears more than once, Claude either supplies a longer string with enough surrounding context to pin down one occurrence, or sets `replace_all: true` to replace them all.

Viewing a file with Bash also satisfies the read-before-edit requirement when the command is `cat`, `head`, `tail`, `sed -n 'X,Yp'`, `grep`, `egrep`, or `fgrep` on a single file with no pipes or redirects. Piped output and other Bash commands do not count, and Claude must use Read before editing in those cases.

This affects edit eligibility only, not permissions. [Read and Edit deny rules](https://code.claude.com/docs/en/permissions) also apply to file commands Claude Code recognizes in Bash, such as `cat`, `head`, `tail`, `sed`, and `grep`, but not to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. The set of commands recognized for deny rules is not the same as the read-before-edit list above: for example, `egrep` and `fgrep` count for read-before-edit but are not checked against Read deny rules. For OS-level enforcement that covers every process, [enable the sandbox](https://code.claude.com/docs/en/sandboxing).

## Write tool behavior

The Write tool creates a new file or overwrites an existing one with the full content provided. It does **not** append or merge.

If the target path already exists, Claude must have read that file at least once in the current conversation before overwriting it. A Write to an unread existing file fails with an error. This constraint does not apply to new files. Viewing the file with Bash also satisfies this requirement under the same rules described in the Edit tool behavior above.

For partial changes to an existing file, Claude uses Edit instead of Write.

## NotebookEdit tool behavior

NotebookEdit modifies a Jupyter notebook one cell at a time, targeting cells by their `cell_id`. It does not perform string replacement across the notebook the way Edit does on plain files.

Three edit modes control what happens to the target cell:

- `replace`: overwrite the cell's source. This is the default.
- `insert`: add a new cell after the target. With no `cell_id`, the new cell goes at the start of the notebook. Requires `cell_type` set to `code` or `markdown`.
- `delete`: remove the target cell.

Permission rules use the `Edit(...)` path format. A rule like `Edit(notebooks/**)` covers NotebookEdit calls on files in that directory.

## Glob tool behavior

The Glob tool finds files by name pattern. It supports standard glob syntax including `**` for recursive directory matching:

- `**/*.js` matches all `.js` files at any depth
- `src/**/*.ts` matches all `.ts` files under `src/`
- `*.{json,yaml}` matches `.json` and `.yaml` files in the current directory

Results are sorted by modification time and capped at 100 files. If the cap is hit, Claude sees a truncation flag in the result and can narrow the pattern.

Glob does **not** respect `.gitignore` by default, so it finds gitignored files alongside tracked ones. This differs from Grep, which skips gitignored files. To make Glob respect `.gitignore`, set `CLAUDE_CODE_GLOB_NO_IGNORE=false` before launching Claude Code.

## Grep tool behavior

The Grep tool searches file contents for patterns. Where Glob finds files by name, Grep finds lines inside them.

Grep is built on [ripgrep](https://github.com/BurntSushi/ripgrep) and uses ripgrep's regex syntax, not POSIX grep. Patterns that include regex metacharacters need escaping. For example, finding `interface{}` in Go code takes the pattern `interface\{\}`.

Three output modes control what comes back:

- `files_with_matches`: file paths only, no line content. This is the default.
- `content`: matching lines with file and line number.
- `count`: match count per file.

Claude can scope results by file with the `glob` parameter, such as `**/*.tsx`, or by language with the `type` parameter, such as `py` or `rust`. By default, patterns match within a single line. Claude can set `multiline: true` to match across line boundaries.

Grep respects `.gitignore`, so gitignored files are skipped. To search a gitignored file, Claude passes its path directly.

**Source**: https://code.claude.com/docs/en/tools-reference
**Last Updated**: 2026-06-13
**Status**: Active
