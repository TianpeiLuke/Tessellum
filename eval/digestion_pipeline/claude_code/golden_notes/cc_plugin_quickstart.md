---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - quickstart
keywords:
  - plugin quickstart
  - claude-plugin plugin.json manifest
  - skills SKILL.md
  - plugin-dir flag
  - claude plugin init
  - skills-directory plugin
  - reload-plugins
  - convert configuration to plugin
  - $ARGUMENTS placeholder
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugins
access_control_group: ["general"]
---

# Claude Code — Plugin Quickstart and Migration

## Overview

This note is the hands-on procedure for building, testing, and migrating a Claude Code plugin. Three workflows are covered: (1) the **quickstart** — create a plugin directory, add a `.claude-plugin/plugin.json` manifest, ship a skill, and load it locally with `--plugin-dir`; (2) **skills-directory development** — let `claude plugin init` scaffold a plugin under your skills directory so Claude Code auto-loads it with no install step; and (3) **migration** — convert existing `.claude/` skills and hooks into a shareable plugin.

The quickstart deliberately uses the lowest-friction loop: edit files, run `/reload-plugins` to pick up changes without restarting, and invoke the skill under its plugin namespace. For what a plugin is and the plugins-vs-standalone decision, see [Plugins overview](cc_plugins_overview.md); for the on-disk layout, see [Plugin directory structure](cc_plugin_directory_structure.md).

## Prerequisites

- Claude Code installed and authenticated.
- If you don't see the `/plugin` command, update Claude Code to the latest version (see the [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) upgrade instructions).

## Create your first plugin

The quickstart walks through creating a plugin with a custom skill — a manifest, a skill, and a local test via the `--plugin-dir` flag.

1. **Create the plugin directory.** Every plugin lives in its own directory containing your skills, agents, or hooks, optionally alongside a `.claude-plugin/plugin.json` manifest: `mkdir my-first-plugin`.

2. **Create the plugin manifest** at `.claude-plugin/plugin.json`. It defines the plugin's identity — name, description, version — which Claude Code displays in the plugin manager. Create the directory (`mkdir my-first-plugin/.claude-plugin`), then write the manifest:

   ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
   {
     "name": "my-first-plugin",
     "description": "A greeting plugin to learn the basics",
     "version": "1.0.0",
     "author": {
       "name": "Your Name"
     }
   }
   ```

   `name` is the unique identifier and skill namespace (skills are prefixed with it, e.g. `/my-first-plugin:hello`). `description` shows in the plugin manager. `version` is optional — if set, users only receive updates when you bump it; if omitted and the plugin is distributed via git, the commit SHA is used and every commit counts as a new version. `author` is optional. For additional fields like `homepage`, `repository`, and `license`, see [Plugin manifest schema](cc_plugin_manifest_schema.md).

3. **Add a skill.** Skills live in the `skills/` directory; each is a folder containing a `SKILL.md`. The folder name becomes the skill name, prefixed with the plugin namespace (`hello/` in `my-first-plugin` creates `/my-first-plugin:hello`). Create `mkdir -p my-first-plugin/skills/hello`, then write `my-first-plugin/skills/hello/SKILL.md`:

   ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
   ---
   description: Greet the user with a friendly message
   disable-model-invocation: true
   ---

   Greet the user warmly and ask how you can help them today.
   ```

4. **Test your plugin.** Run Claude Code with the `--plugin-dir` flag to load it without installing: `claude --plugin-dir ./my-first-plugin`. Once it starts, invoke the skill with `/my-first-plugin:hello`. Claude responds with a greeting, and `/help` lists the skill under the plugin namespace. Plugin skills are **always namespaced** (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name; change the prefix by updating the `name` field in `plugin.json`.

5. **Add skill arguments.** Make the skill dynamic with the `$ARGUMENTS` placeholder, which captures any text the user provides after the skill name. Update `SKILL.md`:

   ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
   ---
   description: Greet the user with a personalized message
   ---

   # Hello Skill

   Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
   ```

   Run `/reload-plugins` to pick up the changes, then try `/my-first-plugin:hello Alex` and Claude greets you by name. For more on passing arguments, see [Skills](https://code.claude.com/docs/en/skills).

The result: a plugin manifest (`.claude-plugin/plugin.json`) describing metadata, a skills directory (`skills/`) holding the custom skill, and skill arguments (`$ARGUMENTS`) for dynamic behavior. The `--plugin-dir` flag is for development and testing; when ready to share, see [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

## Test your plugins locally

The `--plugin-dir` flag loads a plugin directly during development without requiring installation (e.g. `claude --plugin-dir ./my-plugin`). Key behaviors:

- The flag also accepts a `.zip` archive of the plugin directory (`claude --plugin-dir ./my-plugin.zip`), which requires Claude Code v2.1.128 or later.
- When a `--plugin-dir` plugin has the **same name** as an installed marketplace plugin, the local copy takes precedence for that session — letting you test changes without uninstalling first. The exception: plugins that managed settings force-enable or force-disable cannot be overridden by `--plugin-dir`.
- Load **multiple** plugins by repeating the flag: `claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`.
- As you make changes, run `/reload-plugins` to pick up updates without restarting. This reloads plugins, skills, agents, hooks, plugin MCP servers, and plugin LSP servers. Then verify: try skills with `/plugin-name:skill-name`, check agents appear in `/agents`, and verify hooks behave as expected.

To test a plugin already packaged as a `.zip` and hosted at a URL (e.g. a CI build artifact), use `--plugin-url` instead. Claude Code fetches the archive at startup and loads it for that session only; if the fetch fails or the archive is invalid, it reports a plugin load error and starts without it. The same [trust considerations](https://code.claude.com/docs/en/discover-plugins) apply — only point this flag at archives you control or trust. Repeat the flag for multiple URLs, or pass space-separated URLs as one quoted argument.

## Develop a plugin in your skills directory

Instead of passing `--plugin-dir` on every launch, keep a plugin in your skills directory and have Claude Code load it automatically. `claude plugin init` scaffolds one:

```bash theme={null}
claude plugin init my-tool
```

This creates `~/.claude/skills/my-tool/` with a `.claude-plugin/plugin.json` manifest and a starter `SKILL.md`. On the next session it loads as `my-tool@skills-dir` with no marketplace or install step. For the auto-load rules, personal vs. project scope, the workspace-trust requirement, and how to update or remove one, see [Plugin CLI commands](cc_plugin_cli_commands.md).

## Convert existing configurations to plugins

If you already have skills or hooks in your `.claude/` directory, you can convert them into a plugin for easier sharing and distribution.

### Migration steps

1. **Create the plugin structure.** `mkdir -p my-plugin/.claude-plugin`, then create the manifest at `my-plugin/.claude-plugin/plugin.json`:

   ```json my-plugin/.claude-plugin/plugin.json theme={null}
   {
     "name": "my-plugin",
     "description": "Migrated from standalone configuration",
     "version": "1.0.0"
   }
   ```

2. **Copy your existing files** into the plugin directory: `cp -r .claude/commands my-plugin/`, and likewise `cp -r .claude/agents my-plugin/` and `cp -r .claude/skills my-plugin/` if present.

3. **Migrate hooks.** If you have hooks in your settings, create a hooks directory (`mkdir my-plugin/hooks`) and write `my-plugin/hooks/hooks.json`. Copy the `hooks` object from your `.claude/settings.json` or `settings.local.json` — the format is the same. The command receives hook input as JSON on stdin, so use `jq` to extract the file path:

   ```json my-plugin/hooks/hooks.json theme={null}
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
         }
       ]
     }
   }
   ```

4. **Test your migrated plugin** with `claude --plugin-dir ./my-plugin`, then test each component: run your commands, check agents appear in `/agents`, and verify hooks trigger correctly.

After migrating, remove the original files from `.claude/` to avoid duplicates. Project and user `.claude/agents/` definitions override same-named plugin agents, so the plugin version only takes effect once the originals are removed.

### What changes when migrating

| Standalone (`.claude/`)       | Plugin                           |
| :---------------------------- | :------------------------------- |
| Only available in one project | Can be shared via marketplaces   |
| Files in `.claude/commands/`  | Files in `plugin-name/commands/` |
| Hooks in `settings.json`      | Hooks in `hooks/hooks.json`      |
| Must manually copy to share   | Install with `/plugin install`   |

**Source**: https://code.claude.com/docs/en/plugins
**Last Updated**: 2026-06-13
**Status**: Active
