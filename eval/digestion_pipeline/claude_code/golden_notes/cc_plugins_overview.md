---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - extensibility
keywords:
  - claude code plugin
  - self-contained directory
  - plugins vs standalone
  - skill namespacing
  - plugin namespace
  - .claude-plugin
  - share with teammates
  - versioned releases
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/plugins
access_control_group: ["general"]
---

# Claude Code — Plugins Overview

## Overview

A **plugin** is a self-contained directory of components that extends Claude Code with custom functionality. Plugin components include **skills, agents, hooks, MCP servers, LSP servers, and monitors**. Plugins let you package this functionality so it can be shared across projects and teams, version-controlled, and distributed through a marketplace.

Plugins are one of two ways Claude Code supports adding custom skills, agents, and hooks; the other is **standalone configuration** in a `.claude/` directory. The defining difference is packaging and namespacing: a standalone skill is invoked with a short name like `/hello`, while a plugin's skills are always namespaced under the plugin name (`/plugin-name:hello`). This note covers what a plugin is and when to choose each approach. To build one, see [Plugin Quickstart](cc_plugin_quickstart.md); for the on-disk layout, [Plugin Directory Structure](cc_plugin_directory_structure.md); for the manifest, [Plugin Manifest Schema](cc_plugin_manifest_schema.md); and for each component type, [Plugin Components](cc_plugin_components.md).

## When to use plugins vs standalone configuration

Claude Code supports two ways to add custom skills, agents, and hooks:

| Approach                                          | Skill names          | Best for                                                                                        |
| :------------------------------------------------ | :------------------- | :---------------------------------------------------------------------------------------------- |
| **Standalone** (`.claude/` directory)             | `/hello`             | Personal workflows, project-specific customizations, quick experiments                          |
| **Plugins** (self-contained directories with skills, agents, hooks, or a `.claude-plugin/plugin.json` manifest) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

**Use standalone configuration when**:

* You're customizing Claude Code for a single project
* The configuration is personal and doesn't need to be shared
* You're experimenting with skills or hooks before packaging them
* You want short skill names like `/hello` or `/deploy`

**Use plugins when**:

* You want to share functionality with your team or community
* You need the same skills/agents across multiple projects
* You want version control and easy updates for your extensions
* You're distributing through a marketplace
* You're okay with namespaced skills like `/my-plugin:hello` (namespacing prevents conflicts between plugins)

A common workflow is to start with standalone configuration in `.claude/` for quick iteration, then convert to a plugin when you're ready to share.

## Namespacing

Plugin skills are always namespaced (like `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have skills with the same name. The namespace prefix comes from the `name` field in the plugin's `.claude-plugin/plugin.json` manifest — changing that field changes the prefix. Namespacing also applies to other components: for example, the agent `agent-creator` in a plugin named `plugin-dev` appears in the UI as `plugin-dev:agent-creator`.

**Source**: https://code.claude.com/docs/en/plugins
**Last Updated**: 2026-06-13
**Status**: Active
