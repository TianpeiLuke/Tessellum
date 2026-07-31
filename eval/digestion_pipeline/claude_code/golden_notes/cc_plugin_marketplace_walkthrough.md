---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplace
keywords:
  - plugin marketplace walkthrough
  - create a local marketplace
  - marketplace.json catalog
  - plugin.json manifest
  - SKILL.md skill
  - plugin marketplace add
  - plugin install
  - plugin validate
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugin-marketplaces
access_control_group: ["general"]
---

# Claude Code — Plugin Marketplace Walkthrough

## Overview

A **plugin marketplace** is a catalog that lets you distribute plugins to others, providing centralized discovery, version tracking, automatic updates, and support for multiple source types (git repositories, local paths, and more). This note walks through the end-to-end procedure of building one: creating the directory structure, adding a skill, authoring the `plugin.json` manifest and `marketplace.json` catalog, then adding, installing, and running the plugin — closing with how to validate the marketplace before you share it.

At a high level, creating and distributing a marketplace involves four steps: (1) **create plugins** with skills, agents, hooks, MCP servers, or LSP servers — see [Create plugins](https://code.claude.com/docs/en/plugins); (2) **create a marketplace file** — a [`marketplace.json`](cc_marketplace_json_schema.md) listing your plugins and where to find them; (3) **host the marketplace** by pushing to GitHub, GitLab, or another git host; and (4) **share with users**, who add it with `/plugin marketplace add` and install individual plugins. Once live, you update the marketplace by pushing changes; users refresh their local copy with `/plugin marketplace update`.

## Walkthrough: create a local marketplace

This example creates a marketplace with one plugin: a `quality-review` skill for code reviews. You create the directory structure, add a skill, create the plugin manifest and marketplace catalog, then install and test it.

**Step 1 — Create the directory structure.** A marketplace holds a `.claude-plugin/` directory, and each plugin nests its own `.claude-plugin/` plus component directories (here, a `skills/quality-review/` folder):

```bash
mkdir -p my-marketplace/.claude-plugin
mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
```

**Step 2 — Create the skill.** Add a `SKILL.md` file that defines what the `quality-review` skill does. Its YAML frontmatter carries `description` and `disable-model-invocation`:

```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md
---
description: Review code for bugs, security, and performance
disable-model-invocation: true
---

Review the code I've selected or the recent changes for:
- Potential bugs or edge cases
- Security concerns
- Performance issues
- Readability improvements

Be concise and actionable.
```

**Step 3 — Create the plugin manifest.** Add a `plugin.json` that describes the plugin; the manifest goes in the plugin's `.claude-plugin/` directory:

```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json
{
  "name": "quality-review-plugin",
  "description": "Adds a quality-review skill for quick code reviews",
  "version": "1.0.0"
}
```

> Setting `version` means users only receive updates when you change this field, so bump it on every release. If you omit `version` and host this marketplace in git, every commit automatically counts as a new version (see [version resolution](cc_host_and_manage_marketplaces.md) to choose the right approach).

**Step 4 — Create the marketplace file.** Add the catalog that lists your plugin. It declares the marketplace `name`, an `owner`, and a `plugins` array; each entry has at minimum a `name` and a `source` (here a relative path) — see [marketplace.json schema](cc_marketplace_json_schema.md):

```json my-marketplace/.claude-plugin/marketplace.json
{
  "name": "my-plugins",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "quality-review-plugin",
      "source": "./plugins/quality-review-plugin",
      "description": "Adds a quality-review skill for quick code reviews"
    }
  ]
}
```

**Step 5 — Add and install.** Add the marketplace from its local path, then install the plugin (the `@my-plugins` suffix names the marketplace it came from):

```shell
/plugin marketplace add ./my-marketplace
/plugin install quality-review-plugin@my-plugins
```

**Step 6 — Try it out.** Select some code in your editor and run the new skill. Plugin skills are namespaced with the plugin name:

```shell
/quality-review-plugin:quality-review
```

To learn more about what plugins can do — hooks, agents, MCP servers, and LSP servers — see [Plugins](https://code.claude.com/docs/en/plugins).

> **How plugins are installed**: when users install a plugin, Claude Code copies the plugin directory to a cache location, so plugins cannot reference files outside their directory using paths like `../shared-utils` (those files are not copied). To share files across plugins, use symlinks (see [Plugin caching and file resolution](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)).

## Validation and testing

Test your marketplace before sharing it. Validate the marketplace JSON syntax with `claude plugin validate .` (or `/plugin validate .` from within Claude Code). Then add it for testing with `/plugin marketplace add ./path/to/marketplace` and install a test plugin with `/plugin install test-plugin@marketplace-name` to verify everything works. For complete plugin testing workflows, see [Test your plugins locally](https://code.claude.com/docs/en/plugins#test-your-plugins-locally); for technical troubleshooting, see [Plugins reference](https://code.claude.com/docs/en/plugins-reference).

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
