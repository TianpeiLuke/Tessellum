---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - hooks
keywords:
  - hook configuration settings
  - allowmanagedhooksonly
  - allowedhttphookurls
  - httphookallowedenvvars
  - disableallhooks
  - http hook url allowlist
  - managed hooks only
  - hook gating
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Hook Configuration Settings

## Overview

Claude Code exposes four `settings.json` keys that gate **which hooks are allowed to run and what HTTP hooks can access**: `allowManagedHooksOnly`, `allowedHttpHookUrls`, `httpHookAllowedEnvVars`, and `disableAllHooks`. These are policy controls, not hook definitions — the hook *format* (events, matchers, commands) lives in the [hooks documentation](https://code.claude.com/docs/en/hooks). `allowManagedHooksOnly` can only be configured in [managed settings](cc_managed_settings.md); the URL and env-var allowlists can be set at any settings level and **merge across sources**.

This note documents the four hook-gating settings and their behavior. For the hook authoring format, see the hooks reference (B07A, link-out above).

## `allowManagedHooksOnly` (managed only)

`allowManagedHooksOnly` restricts hook loading to vetted sources. When set to `true`:

* Managed hooks and SDK hooks are loaded.
* Hooks from plugins force-enabled in managed settings `enabledPlugins` are loaded. This lets administrators distribute vetted hooks through an organization marketplace while blocking everything else. Trust is granted by full `plugin@marketplace` ID, so a plugin with the same name from a different marketplace stays blocked.
* User hooks, project hooks, and all other plugin hooks are blocked.

Example value: `true`.

## `allowedHttpHookUrls` — restrict HTTP hook URLs

Limit which URLs HTTP hooks can target. Supports `*` as a wildcard for matching. When the array is defined, HTTP hooks targeting non-matching URLs are silently blocked. Hostname matching is case-insensitive and ignores a trailing FQDN dot, matching DNS semantics. `Undefined` = no restriction; an empty array = block all HTTP hooks. **Arrays merge across settings sources.**

```json
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

## `httpHookAllowedEnvVars` — restrict HTTP hook environment variables

Limit which environment variable names HTTP hooks can interpolate into header values. Each hook's effective `allowedEnvVars` is the intersection of its own list and this setting. `Undefined` = no restriction. **Arrays merge across settings sources.**

```json
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

## `disableAllHooks`

`disableAllHooks` (`true`) disables all [hooks](https://code.claude.com/docs/en/hooks) and any custom [status line](https://code.claude.com/docs/en/statusline).

## When hook edits take effect

Claude Code watches your settings files and reloads them when they change, so edits to `hooks` (alongside `permissions` and credential helpers like `apiKeyHelper`) apply to the running session without a restart. The reload covers user, project, local, and managed settings, and the `ConfigChange` hook fires for each detected change.

## Relationship to plugin-only customization

The managed-only `strictPluginOnlyCustomization` key (detailed in [Managed plugin policy settings](cc_managed_plugin_policy_settings.md)) blocks skills, agents, **hooks**, and MCP servers from user and project sources, so they can only come from plugins or managed settings — `true` locks all four surfaces; an array (e.g. `["skills", "hooks"]`) locks only the named ones. It is a broader supply-chain lockdown that overlaps the hook-gating effect of `allowManagedHooksOnly`.

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
