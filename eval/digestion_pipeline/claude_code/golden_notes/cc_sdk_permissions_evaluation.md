---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - permissions
keywords:
  - permission evaluation order
  - allow rules
  - deny rules
  - ask rules
  - disallowed_tools
  - allowed_tools
  - tool-name globs
  - mcp tool naming
  - settings.json permission rules
  - canusetool fallthrough
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/permissions
access_control_group: ["general"]
---

# Claude Agent SDK — How Permissions Are Evaluated

## Overview

The Claude Agent SDK gates every tool request through a fixed, ordered evaluation pipeline before the tool runs. When Claude requests a tool, the SDK consults — in this order — hooks, deny rules, ask rules, the active permission mode, allow rules, and finally the [`canUseTool` callback](https://code.claude.com/docs/en/agent-sdk/user-input). The first step that resolves the request (approve or block) wins; if nothing resolves it, the call falls through to `canUseTool`. This note documents the evaluation order and the **allow / deny rule** semantics. The permission **modes** layer (`default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, `auto`) is its own concept — see the sibling note [cc_sdk_permission_modes](cc_sdk_permission_modes.md). The runtime `canUseTool` approval callback is documented in [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input).

## How permissions are evaluated

When Claude requests a tool, the SDK checks permissions in this order:

1. **Hooks** — run [hooks](cc_sdk_hooks_overview.md) first. A hook can deny the call outright or pass it on. A hook that returns `allow` does **not** skip the deny and ask rules below; those are evaluated regardless of the hook result.
2. **Deny rules** — check `deny` rules (from `disallowed_tools` and [settings.json](https://code.claude.com/docs/en/settings#permission-settings)). If a deny rule matches, the tool is blocked, **even in `bypassPermissions` mode**. Bare-name deny rules like `Bash` remove the tool from Claude's context *before* this evaluation begins, so only scoped rules like `Bash(rm *)` are checked at this step.
3. **Ask rules** — check `ask` rules from settings.json. If an ask rule matches, the call falls through to your `canUseTool` callback for confirmation, **even in `bypassPermissions` mode**. In `dontAsk` mode a matching ask rule is denied instead, because that mode never prompts.
4. **Permission mode** — apply the active [permission mode](cc_sdk_permission_modes.md). `bypassPermissions` approves everything that reaches this step. `acceptEdits` approves file operations. `plan` routes file-edit and shell-write tools to `canUseTool` regardless of allow rules, so write operations cannot be auto-approved while planning. Other modes fall through.
5. **Allow rules** — check `allow` rules (from `allowed_tools` and settings.json). If a rule matches, the tool is approved.
6. **`canUseTool` callback** — if not resolved by any of the above, call your `canUseTool` callback for a decision. In `dontAsk` mode, this step is skipped and the tool is denied.

Hooks, deny rules, and `canUseTool` can route a request down to **Blocked**; permission-mode bypass, allow rules, and `canUseTool` can route it up to **Execute**.

This note focuses on **allow and deny rules** (below) and the permission **modes** layer ([cc_sdk_permission_modes](cc_sdk_permission_modes.md)). For the other two steps:

- **Hooks** — run custom code to allow, deny, or modify tool requests. See [cc_sdk_hooks_overview](cc_sdk_hooks_overview.md).
- **`canUseTool` callback** — prompt users for approval at runtime. See [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input).

## Allow and deny rules

`allowed_tools` and `disallowed_tools` (TypeScript: `allowedTools` / `disallowedTools`) add entries to the allow and deny rule lists in the evaluation flow above. **Allow rules only affect approval:** a tool not listed in `allowed_tools` is still available to Claude and falls through to the permission mode. **Deny rules behave differently** depending on whether they name a tool or scope a pattern within one:

| Option | Effect |
|---|---|
| `allowed_tools=["Read", "Grep"]` | `Read` and `Grep` are auto-approved. Tools not listed here still exist and fall through to the permission mode and `canUseTool`. |
| `disallowed_tools=["Bash"]` | The `Bash` tool definition is removed from the request. Claude does not see the tool and cannot attempt it. |
| `disallowed_tools=["Bash(rm *)"]` | `Bash` stays available. Calls matching `rm *` are denied in every permission mode, including `bypassPermissions`. Other `Bash` calls fall through to the permission mode. |
| `disallowed_tools=["*"]` | Every tool definition is removed from the request. Tool-name globs are supported in deny rules: `"*"` matches every tool and `"mcp__*"` matches every MCP tool across all servers. |

### Allow-rule glob semantics

Allow rules accept tool-name globs **only after a literal `mcp__<server>__` prefix**. The server segment must be glob-free so the rule names a specific server you configured: `mcp__puppeteer__*` matches every tool from the `puppeteer` server, and `mcp__github__get_*` matches its `get_` tools. An unanchored entry like `allowed_tools=["*"]` or `allowed_tools=["mcp__*"]` is **ignored with a startup warning** and does not auto-approve anything.

### Locked-down agent pattern

For a locked-down agent, pair `allowedTools` with `permissionMode: "dontAsk"`. Listed tools are approved; anything else is denied outright instead of prompting:

```typescript
const options = {
  allowedTools: ["Read", "Glob", "Grep"],
  permissionMode: "dontAsk"
};
```

> **`allowed_tools` does not constrain `bypassPermissions`.** `allowed_tools` only pre-approves the tools you list. Unlisted tools are not matched by any allow rule and fall through to the permission mode, where `bypassPermissions` approves them. Setting `allowed_tools=["Read"]` alongside `permission_mode="bypassPermissions"` still approves every tool, including `Bash`, `Write`, and `Edit`. If you need `bypassPermissions` but want specific tools blocked, use `disallowed_tools`.

### Declarative rules in settings.json

You can also configure allow, deny, and ask rules declaratively in `.claude/settings.json`. These rules are read when the `project` setting source is enabled, which it is for default `query()` options. If you set `setting_sources` (TypeScript: `settingSources`) explicitly, include `"project"` for them to apply. See [Permission settings](https://code.claude.com/docs/en/settings#permission-settings) for the rule syntax.

**Source**: https://code.claude.com/docs/en/agent-sdk/permissions
**Last Updated**: 2026-06-13
**Status**: Active
