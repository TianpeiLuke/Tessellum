---
tags:
  - resource
  - documentation
  - claude_code
  - troubleshooting
  - performance
keywords:
  - performance and stability
  - high cpu or memory usage
  - auto-compaction thrashing
  - command hangs or freezes
  - heapdump
  - safe-mode
  - garbled terminal text
  - search and discovery issues
  - wsl slow search
topics:
  - Claude Code
  - Troubleshooting
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/troubleshooting
access_control_group: ["general"]
---

# Claude Code — Performance and Stability Troubleshooting

## Overview

This note covers performance, stability, and search problems once Claude Code is **already running** — high CPU or memory usage, auto-compaction thrashing, hangs, garbled terminal text, and search-tool failures. Each symptom is a short recovery procedure: reduce context pressure, isolate a misbehaving customization, restart without losing the conversation, fix the terminal GPU renderer, or fall back to a system `ripgrep`. Issues that occur *before* a session runs (install/login, configuration, API errors) route to other pages and are linked rather than duplicated here.

If you are not sure which page applies, run `/doctor` inside Claude Code for an automated check of your installation, settings, MCP servers, and context usage. If `claude` will not start at all, run `claude doctor` from your shell instead.

## Performance and Stability

These sections cover issues related to resource usage, responsiveness, and search behavior.

### High CPU or memory usage

Claude Code may consume significant resources when processing large codebases. If you experience performance issues:

1. Use `/compact` regularly to reduce context size.
2. Close and restart Claude Code between major tasks.
3. Consider adding large build directories to your `.gitignore` file.
4. Restart with `claude --safe-mode` to check whether a plugin, MCP server, or hook is the source. It disables all customizations for the session; if usage drops, see [Debug your configuration](https://code.claude.com/docs/en/debug-your-config) to find which one.

If memory usage stays high after these steps, run `/heapdump` to write a JavaScript heap snapshot and a memory breakdown to `~/Desktop`. On Linux without a Desktop folder, the files are written to your home directory.

The breakdown shows resident set size, JS heap, array buffers, and unaccounted native memory, which helps identify whether the growth is in JavaScript objects or in native code. To inspect retainers, open the `.heapsnapshot` file in Chrome DevTools under Memory → Load. Attach both files when reporting a memory issue on [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction stops with a thrashing error

If you see `Autocompact is thrashing: the context refilled to the limit...`, automatic compaction succeeded but a file or tool output immediately refilled the context window several times in a row. Claude Code stops retrying to avoid wasting API calls on a loop that isn't making progress.

To recover:

1. Ask Claude to read the oversized file in smaller chunks, such as a specific line range or function, instead of the whole file.
2. Run `/compact` with a focus that drops the large output, for example `/compact keep only the plan and the diff`.
3. Move the large-file work to a [subagent](https://code.claude.com/docs/en/sub-agents) so it runs in a separate context window.
4. Run `/clear` if the earlier conversation is no longer needed.

### Command hangs or freezes

If Claude Code seems unresponsive:

1. Press Ctrl+C to attempt to cancel the current operation.
2. If still unresponsive, you may need to close the terminal and restart.

Restarting doesn't lose your conversation. Run `claude --resume` in the same directory to pick the session back up.

### Garbled or corrupted text in an editor's integrated terminal

If characters render as boxes, smears, or the wrong glyphs when running Claude Code in the VS Code, Cursor, or Devin Desktop integrated terminal, the terminal's GPU renderer is likely the cause. Run `/terminal-setup` inside Claude Code to set `terminal.integrated.gpuAcceleration` to `"off"`, or set it manually in your editor settings and reload the window. See [Terminal configuration](https://code.claude.com/docs/en/terminal-config) for the other settings `/terminal-setup` writes.

### Search and discovery issues

If the Search tool, `@file` mentions, custom agents, or custom skills aren't finding files, the bundled `ripgrep` binary may not run on your system. Install your platform's `ripgrep` package (for example `brew install ripgrep` on macOS, `sudo apt install ripgrep` on Ubuntu/Debian, `apk add ripgrep` on Alpine, `pacman -S ripgrep` on Arch, or `winget install BurntSushi.ripgrep.MSVC` on Windows) and tell Claude Code to use it instead:

```bash
brew install ripgrep
```

Then set `USE_BUILTIN_RIPGREP=0` in your [environment](https://code.claude.com/docs/en/env-vars).

### Slow or incomplete search results on WSL

Disk read performance penalties when working across file systems on WSL may result in fewer-than-expected matches when using Claude Code on WSL. Search still functions, but returns fewer results than on a native filesystem. `/doctor` will show Search as OK in this case.

**Solutions:**

1. **Submit more specific searches**: reduce the number of files searched by specifying directories or file types: "Search for JWT validation logic in the auth-service package" or "Find use of md5 hash in JS files".
2. **Move project to Linux filesystem**: if possible, ensure your project is located on the Linux filesystem (`/home/`) rather than the Windows filesystem (`/mnt/c/`).
3. **Use native Windows instead**: consider running Claude Code natively on Windows instead of through WSL, for better file system performance.

## Get More Help

If you're experiencing issues not covered here:

1. Run `/doctor` to check installation health, settings validity, MCP configuration, and context usage in one pass.
2. Use the `/feedback` command within Claude Code to report problems directly to Anthropic.
3. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues.
4. Ask Claude directly about its capabilities and features. Claude has built-in access to its documentation.

For symptoms outside performance and stability, route by where you're stuck: `command not found` / install fails / PATH / `EACCES` / TLS errors and login loops / OAuth / `403 Forbidden` / "organization disabled" / Bedrock/Vertex/Foundry credentials go to [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install); settings not applying / hooks not firing / MCP servers not loading go to [Debug your configuration](https://code.claude.com/docs/en/debug-your-config); `API Error: 5xx` / `529 Overloaded` / `429` / request validation / `model not found` go to the [Error reference](https://code.claude.com/docs/en/errors).

**Source**: https://code.claude.com/docs/en/troubleshooting
**Last Updated**: 2026-06-13
**Status**: Active
