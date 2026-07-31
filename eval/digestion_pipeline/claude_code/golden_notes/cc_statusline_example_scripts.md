---
tags:
  - resource
  - documentation
  - claude_code
  - statusline
  - examples
keywords:
  - status line examples
  - context window progress bar
  - git status colors
  - cost and duration tracking
  - multi-line status line
  - jq parse json stdin
  - ansi escape codes
  - used_percentage
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

# Claude Code — Status Line Example Scripts

## Overview

Claude Code's [Examples](https://code.claude.com/docs/en/statusline#examples) section ships ready-to-use status-line scripts that each follow the same contract: read the [session JSON](cc_statusline_json_fields.md) from stdin, extract a few fields, and print a formatted line to stdout. This note covers the four foundational patterns — a context-window progress bar, color-coded git status, cost-and-duration tracking, and a multi-line display. Each ships in Bash, Python, and Node.js; the Bash versions are shown here and the Python/Node.js variants are field-for-field equivalent. The Bash examples use [`jq`](https://jqlang.github.io/jq/) to parse JSON; Python and Node.js have built-in JSON parsing.

To use any example: save the script to a file such as `~/.claude/statusline.sh` (or `.py`/`.js`), make it executable with `chmod +x ~/.claude/statusline.sh`, then add the path to your [`statusLine` settings](cc_statusline_setup.md). The advanced patterns (clickable links, rate limits, caching, Windows) are in [cc_statusline_advanced_examples](cc_statusline_advanced_examples.md).

## Context window usage

Display the current model and context window usage with a visual progress bar. The script reads JSON from stdin, extracts the `used_percentage` field (with a `// 0` fallback for null), and builds a 10-character bar where filled blocks (▓) represent usage and light blocks (░) represent the remainder:

```bash
#!/bin/bash
# Read all of stdin into a variable
input=$(cat)

# Extract fields with jq, "// 0" provides fallback for null
MODEL=$(echo "$input" | jq -r '.model.display_name')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Build progress bar: printf -v creates a run of spaces, then
# ${var// /▓} replaces each space with a block character
BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
[ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

echo "[$MODEL] $BAR $PCT%"
```

The Python variant uses string multiplication (`'▓' * filled`) and `or 0` for null handling; the Node.js variant uses `String.repeat()` and optional chaining (`data.context_window?.used_percentage`).

## Git status with colors

Show the git branch with color-coded indicators for staged and modified files. The script uses [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) for terminal colors — `\033[32m` is green, `\033[33m` is yellow, and `\033[0m` resets — then checks whether the current directory is a git repository, counts staged and modified files, and prints color-coded indicators (`echo -e` enables escape interpretation):

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')

GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
    MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

    GIT_STATUS=""
    [ "$STAGED" -gt 0 ] && GIT_STATUS="${GREEN}+${STAGED}${RESET}"
    [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

    echo -e "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH $GIT_STATUS"
else
    echo "[$MODEL] 📁 ${DIR##*/}"
fi
```

The Python variant shells out via `subprocess.check_output`; the Node.js variant uses `execSync` from `child_process`.

## Cost and duration tracking

Track the session's API cost and elapsed time. `cost.total_cost_usd` accumulates the estimated cost of all API calls in the session, `cost.total_duration_ms` measures total elapsed wall-clock time, and `cost.total_api_duration_ms` tracks only time spent waiting on API responses. The script formats cost as currency and converts milliseconds to minutes and seconds:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

COST_FMT=$(printf '$%.2f' "$COST")
DURATION_SEC=$((DURATION_MS / 1000))
MINS=$((DURATION_SEC / 60))
SECS=$((DURATION_SEC % 60))

echo "[$MODEL] 💰 $COST_FMT | ⏱️ ${MINS}m ${SECS}s"
```

## Display multiple lines

A script can output multiple lines for a richer display — each `echo` (or `print`) statement produces a separate row in the status area. This example combines threshold-based colors (green under 70%, yellow 70–89%, red 90%+), a progress bar, and git branch info across two rows:

```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'

# Pick bar color based on context usage
if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
else BAR_COLOR="$GREEN"; fi

FILLED=$((PCT / 10)); EMPTY=$((10 - FILLED))
printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
BAR="${FILL// /█}${PAD// /░}"

MINS=$((DURATION_MS / 60000)); SECS=$(((DURATION_MS % 60000) / 1000))

BRANCH=""
git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"

echo -e "${CYAN}[$MODEL]${RESET} 📁 ${DIR##*/}$BRANCH"
COST_FMT=$(printf '$%.2f' "$COST")
echo -e "${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
```

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
