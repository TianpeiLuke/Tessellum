---
tags:
  - resource
  - documentation
  - claude_code
  - statusline
  - examples
keywords:
  - status line advanced examples
  - osc 8 clickable links
  - rate limit usage
  - cache expensive operations
  - session_id cache key
  - windows configuration
  - git bash powershell
  - status line script caching
topics:
  - Claude Code
  - Status Line
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/statusline
access_control_group: ["general"]
---

# Claude Code — Advanced Status Line Examples

## Overview

Beyond the basic context/git/cost patterns, the Claude Code `statusline` page provides four advanced status-line recipes that read the same JSON-on-stdin contract but exercise harder edges: **clickable links** (wrapping a repo URL in OSC 8 escape codes), **rate limit usage** (reading the Pro/Max `rate_limits` windows), **caching expensive operations** (throttling slow git calls by keying a temp file on `session_id`), and **Windows configuration** (invoking the command through Git Bash or PowerShell with forward-slash paths). Each recipe is a separate save-the-script-and-point-`statusLine`-at-it procedure on top of the basics in [cc_statusline_example_scripts](cc_statusline_example_scripts.md).

All examples ship in source as a Bash / Python / Node.js triple. This note keeps the Bash form canonical and notes the Python/Node parity in prose. To use any of them: save the script to a file (such as `~/.claude/statusline.sh`), make it executable with `chmod +x`, and add its path to the `statusLine` setting (see [cc_statusline_setup](cc_statusline_setup.md)).

## Clickable links

This recipe builds a clickable link to your GitHub repository. The script gets the git remote URL, converts SSH format to HTTPS with `sed`, and wraps the repo name in **OSC 8 escape sequences** — the format is `\e]8;;URL\a` then the link text then `\e]8;;\a`. Hold `Cmd` (macOS) or `Ctrl` (Windows/Linux) and click to open the link in your browser.

The Bash version uses `printf '%b'`, which interprets backslash escapes more reliably than `echo -e` across different shells:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')

# Convert git SSH URL to HTTPS
REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

if [ -n "$REMOTE" ]; then
    REPO_NAME=$(basename "$REMOTE")
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    # printf %b interprets escape sequences reliably across shells
    printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
else
    echo "[$MODEL]"
fi
```

The Python and Node.js variants do the same work: read the remote with `git remote get-url origin`, rewrite the SSH prefix to HTTPS and strip `.git` (via `re.sub` / `.replace`), then emit the OSC 8 sequence (`\033]8;;…\a…` in Python, `\x1b]8;;…\x07…` in Node). Clickable links require a terminal that supports hyperlinks such as iTerm2, Kitty, or WezTerm.

## Rate limit usage

This recipe displays Claude.ai subscription rate-limit usage. The `rate_limits` object contains a `five_hour` (5-hour rolling) window and a `seven_day` (weekly) window; each window provides `used_percentage` (0–100) and `resets_at` (Unix epoch seconds when the window resets). The field is present only for Claude.ai subscribers (Pro/Max) after the first API response, so each script handles the absent field gracefully — in Bash, `jq`'s `// empty` produces no output when `rate_limits` is absent:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
# "// empty" produces no output when rate_limits is absent
FIVE_H=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
WEEK=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

LIMITS=""
[ -n "$FIVE_H" ] && LIMITS="5h: $(printf '%.0f' "$FIVE_H")%"
[ -n "$WEEK" ] && LIMITS="${LIMITS:+$LIMITS }7d: $(printf '%.0f' "$WEEK")%"

[ -n "$LIMITS" ] && echo "[$MODEL] | $LIMITS" || echo "[$MODEL]"
```

The Python and Node.js variants guard each window with a `None`/`!= null` check (`rate.get('five_hour', {}).get('used_percentage')` / `data.rate_limits?.five_hour?.used_percentage`) and join only the windows that are present, falling back to just the model name when neither is.

## Cache expensive operations

A status-line script runs frequently during active sessions, and commands like `git status` or `git diff` can be slow — especially in large repositories. This recipe caches git information to a temp file and refreshes it only every 5 seconds.

The cache filename must be **stable across invocations within one session but unique across sessions**, so concurrent sessions in different repositories don't read each other's cached git state. Process-based identifiers (`$$`, `os.getpid()`, `process.pid`) change on every invocation and defeat the cache. Use the `session_id` from the JSON input instead: it is stable for the lifetime of a session and unique per session.

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
SESSION_ID=$(echo "$input" | jq -r '.session_id')

CACHE_FILE="/tmp/statusline-git-cache-$SESSION_ID"
CACHE_MAX_AGE=5  # seconds

cache_is_stale() {
    [ ! -f "$CACHE_FILE" ] || \
    # stat -f %m is macOS, stat -c %Y is Linux
    [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
}

if cache_is_stale; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        BRANCH=$(git branch --show-current 2>/dev/null)
        STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
    else
        echo "||" > "$CACHE_FILE"
    fi
fi

IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

if [ -n "$BRANCH" ]; then
    echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
else
    echo "[$MODEL] 📁 ${DIR##*/}"
fi
```

The Python and Node.js variants check staleness with `os.path.getmtime` / `fs.statSync(...).mtimeMs` against `time.time()` / `Date.now()`, run the git commands only when the cache is stale, and write the branch/staged/modified counts to the same `/tmp/statusline-git-cache-{session_id}` file before reading them back. This caching pattern is also recommended as a tip in [cc_statusline_troubleshooting](cc_statusline_troubleshooting.md).

## Windows configuration

On Windows, Claude Code runs status-line commands through **Git Bash** when Git Bash is installed, or through **PowerShell** when Git Bash is absent.

Git Bash treats unquoted backslashes as escape characters, so a Windows-style path such as `C:\Users\username\script.mjs` reaches the script runner with its separators removed and the command fails without a visible error. Write file paths in the `command` string with **forward slashes**, as shown below; the `~` shorthand also works and expands to your Windows home directory.

To run a PowerShell script as your status line, invoke it via `powershell`. This works whether Claude Code routes the command through Git Bash or PowerShell:

```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File C:/Users/username/.claude/statusline.ps1"
  }
}
```

The companion `statusline.ps1` reads stdin with `$input | Out-String | ConvertFrom-Json`, pulls `cwd`, `model.display_name`, and `context_window.used_percentage` off the parsed object, takes the leaf folder with `Split-Path $cwd -Leaf`, and `Write-Host`s a line (with or without the context percentage depending on whether `$used` is set). Alternatively, when Git Bash is installed you can point `command` directly at `~/.claude/statusline.sh` and run a Bash script; the source's Bash variant parses the JSON with `grep -o`/`cut` instead of `jq` to avoid requiring `jq` on Windows.

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
