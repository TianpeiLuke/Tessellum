---
tags:
  - resource
  - documentation
  - claude_code
  - status_line
  - setup
keywords:
  - status line setup
  - statusLine setting
  - /statusline command
  - command type
  - padding refreshinterval
  - hidevimmodeindicator
  - how status lines work
  - debounce 300ms
  - columns lines sizing
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

# Set Up a Claude Code Status Line

## Overview

The status line is a customizable bar at the bottom of Claude Code that runs any shell script you configure. It receives JSON session data on stdin and displays whatever your script prints, giving a persistent, at-a-glance view of context usage, costs, git status, or anything else you want to track. Status lines are useful when you want to monitor context window usage as you work, track session costs, distinguish multiple sessions, or keep git branch and status always visible.

This note covers the two setup paths (the `/statusline` command versus a manual `statusLine` settings field), the step-by-step build, and how the data flows from Claude Code to your script.

## Set up a status line

Use the `/statusline` command to have Claude Code generate a script for you, or manually create a script and add it to your settings.

### Use the /statusline command

The `/statusline` command accepts natural language instructions describing what you want displayed. Claude Code generates a script file in `~/.claude/` and updates your settings automatically:

```text
/statusline show model name and context percentage with a progress bar
```

### Manually configure a status line

Add a `statusLine` field to your user settings (`~/.claude/settings.json`) or [project settings](https://code.claude.com/docs/en/settings#settings-files). Set `type` to `"command"` and point `command` to a script path or an inline shell command:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

The `command` field runs in a shell, so you can also use inline commands instead of a script file (for example, piping the JSON through `jq`).

Optional fields:

- **`padding`** — adds extra horizontal spacing (in characters), in addition to the interface's built-in spacing, so it controls relative indentation rather than absolute distance from the terminal edge. Defaults to `0`.
- **`refreshInterval`** — re-runs the command every N seconds *in addition* to event-driven updates. Minimum is `1`. Set this for time-based data (a clock) or when background subagents change git state while the main session is idle. Leave unset to run only on events.
- **`hideVimModeIndicator`** — set to `true` to suppress the built-in `-- INSERT --` text when your script renders `vim.mode` itself, so the mode is not shown twice.

### Disable the status line

Run `/statusline` and ask it to remove or clear the status line (e.g., `/statusline delete`, `/statusline clear`, `/statusline remove it`). You can also manually delete the `statusLine` field from your settings.json.

## Build a status line step by step

Running `/statusline` configures all of this automatically, but the manual walkthrough shows what happens under the hood — a status line displaying the model, working directory, and context window usage percentage. The examples use Bash (macOS/Linux); Windows uses PowerShell or Git Bash.

1. **Create a script that reads JSON and prints output.** Claude Code sends JSON to stdin; this script uses `jq` to extract fields, then prints a formatted line. Save it to `~/.claude/statusline.sh`:

   ```bash
   #!/bin/bash
   # Read JSON data that Claude Code sends to stdin
   input=$(cat)

   # Extract fields using jq
   MODEL=$(echo "$input" | jq -r '.model.display_name')
   DIR=$(echo "$input" | jq -r '.workspace.current_dir')
   # The "// 0" provides a fallback if the field is null
   PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

   # Output the status line - ${DIR##*/} extracts just the folder name
   echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
   ```

2. **Make it executable** so the shell can run it:

   ```bash
   chmod +x ~/.claude/statusline.sh
   ```

3. **Add to settings.** Set `type` to `"command"` and point `command` at the script in `~/.claude/settings.json`. The status line appears at the bottom; settings reload automatically, but changes won't appear until the next interaction with Claude Code.

## How status lines work

Claude Code runs your script and pipes JSON session data to it via stdin. Your script reads the JSON, extracts what it needs, and prints text to stdout, which Claude Code displays.

**When it updates** — the script runs after each new assistant message, after `/compact` finishes, when the permission mode changes, or when vim mode toggles. Updates are debounced at 300ms, so rapid changes batch together and the script runs once things settle. If a new update triggers while the script is still running, the in-flight execution is cancelled. Edits to the script won't appear until the next interaction triggers an update. These triggers can go quiet when the main session is idle (for example, while a coordinator waits on background subagents); set `refreshInterval` to also re-run on a fixed timer during idle periods.

**What your script can output** — multiple lines (each `echo`/`print` is a separate row), colors via ANSI escape codes like `\033[32m` (the terminal must support them), and links via OSC 8 escape sequences making text clickable (requires a hyperlink-capable terminal like iTerm2, Kitty, or WezTerm).

**Sizing output to the terminal** — Claude Code captures your script's output rather than connecting it to the terminal, so `tput cols` and language-level width detection cannot read the terminal size from inside the script. Read the `COLUMNS` and `LINES` environment variables instead; Claude Code sets these to the current terminal dimensions before running the script (requires v2.1.153 or later).

The status line runs locally and does not consume API tokens. It temporarily hides during certain UI interactions, including autocomplete suggestions, the help menu, and permission prompts.

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
