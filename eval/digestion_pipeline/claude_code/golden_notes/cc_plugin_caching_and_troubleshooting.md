---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - troubleshooting
keywords:
  - plugin cache
  - path traversal
  - symlink resolution
  - claude --debug
  - plugin troubleshooting
  - manifest validation errors
  - mcp server troubleshooting
  - code intelligence issues
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugins-reference
access_control_group: ["general"]
---

# Claude Code Plugin Caching and Troubleshooting

## Overview

When a plugin is installed from a marketplace, Claude Code copies it into a local **plugin cache** (`~/.claude/plugins/cache`) rather than running it in place, isolating the cached copy and enforcing path-traversal and symlink rules for security. This note covers that caching/file-resolution model and the procedure for diagnosing a plugin that does not load, whose hooks or MCP servers fail, or whose LSP code intelligence misbehaves — using `claude --debug` and the common-issue / error-message reference tables.

Caching and file resolution come from the `plugins-reference` page; the debugging command, common-issues, error-message, and hook/MCP/structure checklists come from the same page's "Debugging and development tools"; the `/plugin`-recognition and code-intelligence fixes come from the `discover-plugins` "Troubleshooting" section. Plugin authoring, install scopes, and version management are covered by sibling notes; see [Related Notes](#related-notes).

## Plugin Caching and File Resolution

Plugins are specified in one of two ways:

- Through `claude --plugin-dir` or `claude --plugin-url`, for the duration of a session.
- Through a marketplace, installed for future sessions.

For security and verification purposes, Claude Code copies *marketplace* plugins to the user's local **plugin cache** (`~/.claude/plugins/cache`) rather than using them in-place. Understanding this behavior is important when developing plugins that reference external files.

Each installed version is a separate directory in the cache. When you update or uninstall a plugin, the previous version directory is marked as orphaned and removed automatically **7 days later**. The grace period lets concurrent Claude Code sessions that already loaded the old version keep running without errors. Claude's Glob and Grep tools skip orphaned version directories during searches, so file results don't include outdated plugin code.

### Path traversal limitations

Installed plugins cannot reference files outside their directory. Paths that traverse outside the plugin root (such as `../shared-utils`) will not work after installation because those external files are not copied to the cache.

### Share files within a marketplace with symlinks

If your plugin needs to share files with other parts of the same marketplace, you can create symbolic links inside your plugin directory. How a symlink is handled when the plugin is copied into the cache depends on where its target resolves:

- **Within the plugin's own directory:** the symlink is preserved as a relative symlink in the cache, so it keeps resolving to the copied target at runtime.
- **Elsewhere within the same marketplace:** the symlink is dereferenced — the target's content is copied into the cache in its place. This lets a meta-plugin's `skills/` directory link to skills defined by other plugins in the marketplace.
- **Outside the marketplace:** the symlink is skipped for security. This prevents plugins from pulling arbitrary host files such as system paths into the cache.

For plugins installed with `--plugin-dir` or from a local path, only symlinks that resolve within the plugin's own directory are preserved; all others are skipped. To link to a shared skill defined by a sibling plugin (on Windows, use `mklink /D` from an elevated Command Prompt or enable Developer Mode):

```bash
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

## Debugging and Development Tools

### Debugging commands

Use `claude --debug` to see plugin loading details. This shows:

- Which plugins are being loaded
- Any errors in plugin manifests
- Skill, agent, and hook registration
- MCP server initialization

### Common issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| Plugin not loading | Invalid `plugin.json` | Run `claude plugin validate` or `/plugin validate` to check `plugin.json`, skill/agent/command frontmatter, and `hooks/hooks.json` for syntax and schema errors |
| Skills not appearing | Wrong directory structure | Ensure `skills/` or `commands/` is at the plugin root, not inside `.claude-plugin/` |
| Hooks not firing | Script not executable | Run `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths |
| Path errors | Absolute paths used | All paths must be relative and start with `./` |
| LSP `Executable not found in $PATH` | Language server not installed | Install the binary (e.g., `npm install -g typescript-language-server typescript`) |

### Example error messages

**Manifest validation errors:**

- `Invalid JSON syntax: Unexpected token } in JSON at position 142`: check for missing commas, extra commas, or unquoted strings.
- `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: a required field is missing.
- `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON syntax error.

**Plugin loading errors:**

- `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: command path exists but contains no valid command files.
- `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: the `source` path in marketplace.json points to a non-existent directory.
- `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: remove duplicate component definitions or remove `strict: false` in marketplace entry.

### Hook troubleshooting

**Hook script not executing:**

1. Check the script is executable: `chmod +x ./scripts/your-script.sh`
2. Verify the shebang line: first line should be `#!/bin/bash` or `#!/usr/bin/env bash`
3. Check the path uses `${CLAUDE_PLUGIN_ROOT}`: `"command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/your-script.sh"`
4. Test the script manually: `./scripts/your-script.sh`

**Hook not triggering on expected events:**

1. Verify the event name is correct (case-sensitive): `PostToolUse`, not `postToolUse`
2. Check the matcher pattern matches your tools: `"matcher": "Write|Edit"` for file operations
3. Confirm the hook type is valid: `command`, `http`, `mcp_tool`, `prompt`, or `agent`

### MCP server troubleshooting

**Server not starting:**

1. Check the command exists and is executable
2. Verify all paths use `${CLAUDE_PLUGIN_ROOT}` variable
3. Check the MCP server logs: `claude --debug` shows initialization errors
4. Test the server manually outside of Claude Code

**Server tools not appearing:**

1. Ensure the server is properly configured in `.mcp.json` or `plugin.json`
2. Verify the server implements the MCP protocol correctly
3. Check for connection timeouts in debug output

### Directory structure mistakes

**Symptoms:** Plugin loads but components (skills, agents, hooks) are missing.

**Correct structure:** Components must be at the plugin root, not inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`. If your components are inside `.claude-plugin/`, move them to the plugin root.

**Debug checklist:**

1. Run `claude --debug` and look for "loading plugin" messages
2. Check that each component directory is listed in the debug output
3. Verify file permissions allow reading the plugin files

## Marketplace and Install Troubleshooting

### /plugin command not recognized

If you see "unknown command" or the `/plugin` command doesn't appear:

1. **Check your version:** Run `claude --version` to see what's installed.
2. **Update Claude Code:**
   - **Homebrew:** `brew upgrade claude-code` (or `brew upgrade claude-code@latest` if you installed that cask)
   - **npm:** `npm install -g @anthropic-ai/claude-code@latest`
   - **Native installer:** Re-run the install command from Setup
3. **Restart Claude Code:** After updating, restart your terminal and run `claude` again.

### Common issues

- **Marketplace not loading:** Verify the URL is accessible and that `.claude-plugin/marketplace.json` exists at the path.
- **Plugin installation failures:** Check that plugin source URLs are accessible and repositories are public (or you have access).
- **Files not found after installation:** Plugins are copied to a cache, so paths referencing files outside the plugin directory won't work.
- **Plugin skills not appearing:** Clear the cache with `rm -rf ~/.claude/plugins/cache`, restart Claude Code, and reinstall the plugin.

### Code intelligence issues

- **Language server not starting:** verify the binary is installed and available in your `$PATH`. Check the `/plugin` Errors tab for details.
- **High memory usage:** language servers like `rust-analyzer` and `pyright` can consume significant memory on large projects. If you experience memory issues, disable the plugin with `/plugin disable <plugin-name>` and rely on Claude's built-in search tools instead.
- **False positive diagnostics in monorepos:** language servers may report unresolved import errors for internal packages if the workspace isn't configured correctly. These don't affect Claude's ability to edit code.

**Source**: https://code.claude.com/docs/en/plugins-reference
**Last Updated**: 2026-06-13
**Status**: Active
