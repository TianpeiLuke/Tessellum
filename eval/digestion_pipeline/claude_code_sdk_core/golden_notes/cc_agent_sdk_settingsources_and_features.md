---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - settingsources
keywords:
  - settingsources
  - claude.md and rules
  - filesystem features
  - skills loading
  - filesystem vs programmatic hooks
  - choose the right feature
  - multi-tenant isolation
  - claude agent sdk migration
  - claudecodeoptions to claudeagentoptions
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/claude-code-features
access_control_group: ["general"]
---

# Agent SDK — Claude Code Features (settingSources) and Migration

## Overview

The Agent SDK is built on the same foundation as Claude Code, so SDK agents can load the same filesystem-based features: project instructions (`CLAUDE.md` and rules), skills, and hooks. This note is the procedure for *loading* those features via the `settingSources` option, choosing which feature fits a goal, and (folded in) migrating from the old Claude Code SDK to the Claude Agent SDK. When you omit `settingSources`, `query()` reads the same filesystem settings as the Claude Code CLI: user, project, and local settings, `CLAUDE.md` files, and `.claude/` skills, agents, and commands. To run without these, pass `settingSources: []`, which limits the agent to what you configure programmatically.

## Control filesystem settings with settingSources

The setting-sources option (`setting_sources` in Python, `settingSources` in TypeScript) controls which filesystem-based settings the SDK loads. Pass an explicit list to opt in to specific sources, or pass an empty array to disable user, project, and local settings. This Python example loads both user-level and project-level settings:

```python theme={null}
async for message in query(
    prompt="Help me refactor the auth module",
    options=ClaudeAgentOptions(
        setting_sources=["user", "project"],
        allowed_tools=["Read", "Edit", "Bash"],
    ),
):
    ...
```

Each source loads from a specific location, where `<cwd>` is the working directory passed via `cwd` (or the process's current directory):

| Source | What it loads | Location |
|---|---|---|
| `"project"` | Project CLAUDE.md, `.claude/rules/*.md`, project skills, project hooks, project `settings.json` | `<cwd>/.claude/` for `settings.json` and hooks; `<cwd>` and every parent for CLAUDE.md and rules; `<cwd>` and every parent up to the repo root for skills |
| `"user"` | User CLAUDE.md, `~/.claude/rules/*.md`, user skills, user settings | `~/.claude/` |
| `"local"` | CLAUDE.local.md, `.claude/settings.local.json` | `<cwd>/.claude/` for `settings.local.json`; `<cwd>` and every parent for CLAUDE.local.md |

Omitting `settingSources` is equivalent to `["user", "project", "local"]`. CLAUDE.md and rules load from `<cwd>` and every parent directory; skills load from `<cwd>` and every parent up to the repository root; project `settings.json` and hooks load only from `<cwd>/.claude/` with no parent-directory fallback.

### What settingSources does not control

`settingSources` covers user, project, and local settings only. A few inputs are read regardless of its value: **managed policy settings** (always loaded when present; remove the managed settings file to disable), **`~/.claude.json` global config** (always read; relocate with `CLAUDE_CONFIG_DIR`), **auto memory at `~/.claude/projects/<project>/memory/`** (loaded by default into the system prompt; disable with `autoMemoryEnabled: false` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`), and **claude.ai MCP connectors** (loaded when the active auth method is a claude.ai subscription; passing `mcpServers: {}` does not suppress them — set `strictMcpConfig: true` or `ENABLE_CLAUDEAI_MCP_SERVERS=false`).

> **Multi-tenant warning (from source):** Do not rely on default `query()` options for multi-tenant isolation. Because the inputs above are read regardless of `settingSources`, an SDK process can pick up host-level configuration and per-directory memory. For multi-tenant deployments, run each tenant in its own filesystem and set `settingSources: []` plus `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`. See [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment).

## Project instructions (CLAUDE.md and rules)

`CLAUDE.md` files and `.claude/rules/*.md` files give the agent persistent context (conventions, build commands, architecture decisions). When `settingSources` includes `"project"`, the SDK loads these into context at session start. Load locations span project root (`<cwd>/CLAUDE.md` or `<cwd>/.claude/CLAUDE.md`), project rules (`<cwd>/.claude/rules/*.md` and in every parent), parent-dir CLAUDE.md (at session start), child-dir CLAUDE.md (on demand when the agent reads a file in that subtree), local (`CLAUDE.local.md`), and user (`~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`). All levels are **additive** — if both project and user files exist, the agent sees both. There is no hard precedence rule; if instructions conflict, the outcome depends on how Claude interprets them, so write non-conflicting rules or state precedence explicitly in the more specific file. You can also inject context directly via `systemPrompt` instead of CLAUDE.md (see [Modify system prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)).

## Skills

Skills are markdown files that give the agent specialized knowledge and invocable workflows. Unlike CLAUDE.md (loaded every session), skills load **on demand** — the agent receives skill *descriptions* at startup and loads full content when relevant. Skills are discovered from the filesystem through `settingSources`. When the `skills` option is omitted, discovered user and project skills are enabled and the Skill tool is available (matching CLI behavior). To control which are enabled, pass `skills` as `"all"`, a list of names, or `[]` to disable all. When `skills` is set, the SDK adds the Skill tool to `allowedTools` automatically; if you also pass an explicit `tools` list, include `"Skill"` so Claude can invoke skills. Skills must be created as filesystem artifacts (`.claude/skills/<name>/SKILL.md`) — there is no programmatic registration API. Full details: [Agent Skills in the SDK](https://code.claude.com/docs/en/agent-sdk/skills).

## Hooks

The SDK supports two hook types that run side by side: **filesystem hooks** (shell commands in `settings.json`, loaded when `settingSources` includes the relevant source — the same hooks as interactive sessions) and **programmatic hooks** (callback functions passed directly to `query()`, running in your application process and returning structured decisions). Both execute during the same hook lifecycle. Hook callbacks receive the tool input and return a decision dict: returning `{}` allows the tool to proceed; to block, return a `hookSpecificOutput` with `permissionDecision: "deny"` and a `permissionDecisionReason` (the reason is sent to Claude as the tool result). The top-level `decision`/`reason` fields are deprecated for `PreToolUse`. A `PreToolUse` callback that blocks a destructive command:

```python theme={null}
async def audit_bash(input_data, tool_use_id, context):
    command = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf" in command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Destructive command blocked",
            }
        }
    return {}  # Empty dict: allow the tool to proceed
```

### When to use which hook type

| Hook type | Best for |
|---|---|
| **Filesystem** (`settings.json`) | Sharing hooks between CLI and SDK sessions. Supports `"command"` (shell), `"http"` (POST to an endpoint), `"mcp_tool"`, `"prompt"` (LLM evaluates a prompt), and `"agent"` (spawns a verifier agent). Fire in the main agent and any subagents. |
| **Programmatic** (callbacks in `query()`) | Application-specific logic, structured decisions, in-process integration. Also fire inside subagents; the callback receives `agent_id`/`agent_type` to distinguish. |

The TypeScript SDK supports additional hook events beyond Python (`SessionStart`, `SessionEnd`, `TeammateIdle`, `TaskCompleted`). For the hook lifecycle and callback signatures see [cc_agent_sdk_result_and_hooks](cc_agent_sdk_result_and_hooks.md) and the full [hooks guide](https://code.claude.com/docs/en/agent-sdk/hooks).

## Choose the right feature

This table maps a common goal to the right approach and its SDK surface:

| You want to... | Use | SDK surface |
|---|---|---|
| Set project conventions the agent always follows | CLAUDE.md | `settingSources: ["project"]` loads it automatically |
| Give reference material it loads when relevant | Skills | `settingSources` + `skills` option |
| Run a reusable workflow (deploy, review, release) | User-invocable skills | `settingSources` + `skills` option |
| Delegate an isolated subtask to a fresh context | Subagents | `agents` parameter + `allowedTools: ["Agent"]` |
| Coordinate multiple Claude Code instances with shared task lists | Agent teams | Not via SDK options — a CLI feature where one session is team lead |
| Run deterministic logic on tool calls (audit, block, transform) | Hooks | `hooks` parameter with callbacks, or shell scripts via `settingSources` |
| Give Claude structured tool access to an external service | MCP | `mcpServers` parameter |

**Subagents versus agent teams:** subagents are ephemeral and isolated (fresh conversation, one task, summary returned to parent); agent teams coordinate multiple independent Claude Code instances that share a task list and message each other directly (a CLI feature). Every feature you enable adds to the agent's context window.

## Migrate from the old SDK

The **Claude Code SDK** has been renamed to the **Claude Agent SDK**, reflecting its broader capabilities for building agents beyond coding. Package names changed: TS/JS `@anthropic-ai/claude-code` → `@anthropic-ai/claude-agent-sdk`; Python `claude-code-sdk` → `claude-agent-sdk`. Migration steps are symmetric: uninstall the old package, install the new one, and update imports (and in Python, type names). The Python type rename:

```python theme={null}
# BEFORE (claude-code-sdk)
from claude_code_sdk import query, ClaudeCodeOptions
options = ClaudeCodeOptions(model="claude-opus-4-7", permission_mode="acceptEdits")

# AFTER (claude-agent-sdk)
from claude_agent_sdk import query, ClaudeAgentOptions
options = ClaudeAgentOptions(model="claude-opus-4-7", permission_mode="acceptEdits")
```

**Breaking changes (v0.1.0):** (1) Python `ClaudeCodeOptions` renamed to `ClaudeAgentOptions`. (2) **System prompt no longer default** — the SDK uses a minimal system prompt by default; to get the old behavior, request the preset explicitly (`systemPrompt: { type: "preset", preset: "claude_code" }`) or pass a custom string. (3) **Settings sources default** — this default was briefly changed in v0.1.0 and then reverted, so no migration action is needed. Current behavior: omitting `settingSources` loads user, project, and local settings (matching the CLI); pass `[]` to isolate. (Note: Python SDK 0.1.59 and earlier treated an empty list the same as omitting the option, so upgrade before relying on `setting_sources=[]`.) The rename reflects the SDK's evolution from a coding-only tool into a framework for building business agents, specialized coding agents, and custom domain agents.

## Related Notes

### Related Notes (Claude Code Series)
- [Agent SDK — Overview](cc_agent_sdk_overview.md) — relevance: establishes the SDK as "Claude Code as a library" with the same tools, loop, and context management; this note is the procedure for *loading* the filesystem features that "same foundation" makes available.
- [SDK Python Options and Config Types](cc_sdk_python_options_and_config_types.md) — relevance: documents `ClaudeAgentOptions` field-by-field, including the `SettingSource` type and the `skills`/`hooks`/`mcpServers` fields this note operates; the migration section's `ClaudeCodeOptions`→`ClaudeAgentOptions` rename is the same dataclass.
- [SDK System Prompts](cc_sdk_system_prompts.md) — relevance: this note routes "set project conventions" to CLAUDE.md, but `systemPrompt` is the alternative injection path; the migration breaking change "system prompt no longer default" (request the `claude_code` preset) is the same shift that note covers in depth.
- [Loading Agent Skills in the SDK](cc_sdk_skills.md) — relevance: the deep dive on the `skills` option this note summarizes — filesystem discovery via `settingSources`, on-demand loading, and auto-adding the `Skill` tool to `allowedTools`.
- [SDK Hooks — Overview](cc_sdk_hooks_overview.md) — relevance: expands the filesystem-vs-programmatic hook distinction this note introduces, including the block/allow decision dict (`permissionDecision: "deny"`) used in the `PreToolUse` example here.
- [cc_agent_sdk_result_and_hooks](cc_agent_sdk_result_and_hooks.md) — relevance: the loop's hook lifecycle and `ResultMessage` surface that the filesystem/programmatic hooks loaded here plug into.
- [CLAUDE.md Files](cc_claude_md_files.md) — relevance: defines the project-instruction files that `settingSources: ["project"]` loads into context at session start and that the "Project instructions" section here describes loading.
- [SDK Secure Deployment Principles](cc_sdk_secure_deployment_principles.md) — relevance: the isolation/least-privilege framework behind the multi-tenant warning here (`settingSources: []` + disable auto memory + per-tenant filesystem); the warning's "See Secure deployment" link points to this content.

### Related Notes (Out-of-Series)
- [Claude Code](../../term_dictionary/term_claude_code.md) — the Agent SDK loads Claude Code's filesystem features (CLAUDE.md, rules, skills, hooks) into SDK agents and is the renamed-from product; the term anchors both the features and the migration.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — `settingSources` loads CLAUDE.md/rules as persistent project context, and auto memory at `~/.claude/projects/<project>/memory/` is loaded into the system prompt — the agentic-memory persistence mechanism this term defines.
- [Skills](../../term_dictionary/term_skills.md) — skills are discovered via `settingSources`, load on demand (description at start, full content when relevant), and need the `Skill` tool enabled — the skills mechanism this term defines.
- [Sandbox](../../term_dictionary/term_sandbox.md) — the multi-tenant warning (inputs read regardless of `settingSources`; use `settingSources: []` + disable auto memory + per-tenant filesystem) is the isolation/sandboxing guidance this term frames.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — filesystem hooks loaded via `settingSources` can deny tool calls (`permissionDecision: "deny"`), wiring the project's graduated-trust permission rules into the SDK agent.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — the "inputs read regardless" table and the choose-a-feature row both cover MCP servers (claude.ai connectors loaded by subscription auth; `mcpServers` for structured external access) — MCP is one feature this note routes.
- [Schema Evolution](../../term_dictionary/term_schema_evolution.md) — the migration section documents a versioned breaking change (`ClaudeCodeOptions`→`ClaudeAgentOptions`, package rename, default-behavior shifts across v0.0.x→v0.1.0→revert) — the schema/API evolution-and-migration discipline this term defines.
- [Strands Agents](../../tools/tool_strands_agents.md) — relevance: a peer AWS agent-building SDK (model-driven orchestration, multi-agent patterns); the migration section reframes the Claude Agent SDK as exactly this kind of general agent framework, making Strands the closest non-Claude comparator.
- [Vault Project: CLI Agent Configuration](../../../projects/vault_project/vault_project_cli_agent_config.md) — relevance: a concrete agent config that loads all MCP servers and 96 vault skills at startup — the real-world analogue of `settingSources` + `skills` + `mcpServers` feature loading this note specifies.
- [Tutorial Part 4: Configuration & Permissions](../tutorials/tutorial_claude_code_04_configuration.md) — relevance: the CLI-side counterpart to `settingSources` — configuring `CLAUDE.md`, tool permissions, and `settings.json`, the same filesystem settings the SDK reads when `settingSources` is omitted.
- [How To: Set Up Autonomous Maintenance Using Claude Code Skills](../../how_to/howto_autonomous_maintenance_claude.md) — relevance: applies the hooks + skills features this note catalogs (Stop/SessionStart hooks, subagents, scheduled runs) to drive autonomous workflows — the "choose the right feature" table in action.
- [How To: Chain Multiple Claude Code Skills into a Pipeline](../../how_to/howto_chain_claude_skills.md) — relevance: builds on the on-demand skills + subagent-orchestrator features this note describes, showing how `settingSources`-discovered skills are composed into multi-step pipelines.

**Source**: https://code.claude.com/docs/en/agent-sdk/claude-code-features
**Last Updated**: 2026-06-13
**Status**: Active
