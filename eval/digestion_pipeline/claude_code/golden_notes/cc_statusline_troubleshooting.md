---
tags:
  - resource
  - documentation
  - claude_code
  - status_line
  - troubleshooting
keywords:
  - status line troubleshooting
  - mock input testing
  - statusline skipped restart to fix
  - workspace trust required
  - force_hyperlink
  - osc 8 not clickable
  - script errors or hangs
  - cache slow operations
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

# Status Line — Tips & Troubleshooting

## Overview

This note covers the operational tips for writing a reliable status line and the troubleshooting matrix for the common failure modes of a configured `statusLine`. The status line is a shell script Claude Code runs after each turn (see [Set up a status line](cc_statusline_setup.md)), so most problems trace back to the JSON-in / stdout-out contract, the workspace-trust gate, or terminal escape-sequence support. The guidance here is diagnostic: test the script in isolation first, then work through the symptom-specific fixes.

## Tips

- **Test with mock input** — pipe a small fake JSON payload to the script and confirm it produces output before configuring it:

```bash
echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/home/user/project"},"context_window":{"used_percentage":25},"session_id":"test-session-abc"}' | ./statusline.sh
```

- **Keep output short** — the status bar has limited width, so long output may get truncated or wrap awkwardly.
- **Cache slow operations** — the script runs frequently during active sessions, so commands like `git status` can cause lag. Cache slow git operations to a temp file keyed on `session_id` (see [advanced examples](cc_statusline_advanced_examples.md)).

Community projects such as `ccstatusline` and `starship-claude` provide pre-built configurations with themes and additional features.

## Troubleshooting

**Status line not appearing**
- Verify the script is executable: `chmod +x ~/.claude/statusline.sh`.
- Check that the script outputs to stdout, not stderr; run it manually to confirm it produces output.
- On Windows with Git Bash installed, backslashes in the `command` path are consumed as escape characters before the script runs — use forward slashes (see [Windows configuration in the advanced examples](cc_statusline_advanced_examples.md)).
- If `disableAllHooks` is `true` in settings, the status line is also disabled. Remove it or set it to `false`.
- Run `claude --debug` to log the exit code and stderr from the first status line invocation in a session.
- Ask Claude to read the settings file and execute the `statusLine` command directly to surface errors.

**Status line shows `--` or empty values**
- Fields may be `null` before the first API response completes — handle nulls with fallbacks such as `// 0` in jq (the field semantics are in [JSON fields](cc_statusline_json_fields.md)).
- Restart Claude Code if values remain empty after multiple messages.

**Context percentage shows unexpected values**
- Use `used_percentage` for the simplest accurate context state.
- Context percentage may differ from `/context` output due to when each is calculated.

**OSC 8 links not clickable**
- Verify the terminal supports OSC 8 hyperlinks (iTerm2, Kitty, WezTerm); Terminal.app does not support clickable links.
- If link text appears but isn't clickable, Claude Code may not have detected hyperlink support (commonly affects Windows Terminal and other emulators not in the auto-detection list). Set `FORCE_HYPERLINK` to override detection before launching (`FORCE_HYPERLINK=1 claude`; in PowerShell, `$env:FORCE_HYPERLINK = "1"; claude`).
- SSH and tmux sessions may strip OSC sequences depending on configuration.
- If escape sequences appear as literal text like `\e]8;;`, use `printf '%b'` instead of `echo -e` for more reliable escape handling.

**Display glitches with escape sequences**
- Complex escape sequences (ANSI colors, OSC 8 links) can occasionally cause garbled output if they overlap with other UI updates.
- If text looks corrupted, simplify the script to plain text output; multi-line status lines with escape codes are more prone to rendering issues than single-line plain text.

**Workspace trust required**
- The status line command only runs if you've accepted the workspace trust dialog for the current directory. Because `statusLine` executes a shell command, it requires the same trust acceptance as hooks and other shell-executing settings.
- If trust isn't accepted, you'll see the notification `statusline skipped · restart to fix` instead of your output. Restart Claude Code and accept the trust prompt to enable it.

**Script errors or hangs**
- Scripts that exit with non-zero codes or produce no output cause the status line to go blank.
- Slow scripts block the status line from updating until they complete — keep scripts fast to avoid stale output.
- If a new update triggers while a slow script is running, the in-flight script is cancelled.
- Test the script independently with mock input before configuring it.

**Notifications share the status line row**
- System notifications (MCP server errors, auto-updates) display on the right side of the same row; transient notifications like the context-low warning also cycle through this area.
- Verbose mode adds a token counter to this area.
- On narrow terminals, these notifications may truncate your status line output.

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
