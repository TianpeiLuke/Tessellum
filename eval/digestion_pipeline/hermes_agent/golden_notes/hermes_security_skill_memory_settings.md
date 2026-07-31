---
tags:
  - resource
  - documentation
  - hermes_agent
  - configuration
  - security
keywords:
  - hermes security settings
  - skill write approval
  - memory write approval
  - tirith scanning
  - smart approvals
  - delegation width depth
  - soul.md agents.md context files
topics:
  - Hermes Agent
  - Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Security, Skill & Memory Configuration

## Overview

This note documents the **safety and agency** cluster of `~/.hermes/config.yaml`: the `config.yaml` blocks that gate what the Hermes agent is allowed to do to itself, to your machine, and to your data. It covers skill-write guards and write approval, memory limits and memory-write approval, PII privacy redaction, the `execute_code` mode, Tirith pre-execution security scanning and secret redaction, the website blocklist, smart approvals, checkpoints, subagent delegation width/depth, the clarify timeout, and the SOUL.md / AGENTS.md context files that define the agent's identity. The feature deep-dives (skills, memory, code execution, checkpoints, security, delegation) are owned by other sub-plans and are link-outs here — this note is the configuration reference for the keys themselves.

## Skill Settings

Skills can declare their own configuration settings via their SKILL.md frontmatter. These are non-secret values (paths, preferences, domain settings) stored under the `skills.config` namespace in `config.yaml` — e.g. `skills.config.myplugin.path: ~/myplugin-data`, where each skill defines its own keys. How skill settings work:

- `hermes config migrate` scans all enabled skills, finds unconfigured settings, and offers to prompt you.
- `hermes config show` displays all skill settings under "Skill Settings" with the skill they belong to.
- When a skill loads, its resolved config values are injected into the skill context automatically.

Set values manually with `hermes config set skills.config.myplugin.path ~/myplugin-data`.

### Guard on agent-created skill writes

When the agent uses `skill_manage` to create, edit, patch, or delete a skill, Hermes can optionally scan the new/updated content for dangerous keyword patterns (credential harvesting, obvious prompt injection, exfil instructions) by setting `skills.guard_agent_created: true` (default `false`). The scanner is **off by default** — real agent workflows that legitimately touch `~/.ssh/` or mention `$OPENAI_API_KEY` were tripping the heuristic too often. When on, any flagged `skill_manage` write surfaces as an approval prompt with the scanner's rationale. Accepted writes land; denied writes return an explanatory error to the agent.

### Write approval for skill writes

Independent of the content scanner above, `skills.write_approval` gates **every** agent skill write (create / edit / patch / delete / supporting files) behind your explicit approval — the same approve/deny mechanism as dangerous commands. When on, skill writes are staged under `~/.hermes/pending/skills/` and reviewed with `/skills pending`, `/skills diff <id>`, `/skills approve <id>`, `/skills reject <id>` from the CLI or any messaging platform. Toggle at runtime with `/skills approval on|off`. Memory has the same gate (`memory.write_approval`, below).

## Memory Configuration

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200   # ~800 tokens
  user_char_limit: 1375     # ~500 tokens
  write_approval: false     # true = require approval before any memory write
```

With `memory.write_approval: true`, memory writes need your approval before they land: interactive CLI turns prompt inline; messaging sessions and the background self-improvement review stage the write for `/memory pending` → `/memory approve <id>` / `/memory reject <id>` review. Toggle at runtime with `/memory approval on|off`.

## Privacy

```yaml
privacy:
  redact_pii: false  # Strip PII from LLM context (gateway only)
```

When `redact_pii` is `true`, the gateway redacts personally identifiable information from the system prompt before sending it to the LLM on supported platforms:

| Field | Treatment |
|-------|-----------|
| Phone numbers (user ID on WhatsApp/Signal) | Hashed to `user_<12-char-sha256>` |
| User IDs | Hashed to `user_<12-char-sha256>` |
| Chat IDs | Numeric portion hashed, platform prefix preserved (`telegram:<hash>`) |
| Home channel IDs | Numeric portion hashed |
| User names / usernames | **Not affected** (user-chosen, publicly visible) |

**Platform support:** Redaction applies to WhatsApp, Signal, and Telegram. Discord and Slack are excluded because their mention systems (`<@user_id>`) require the real ID in the LLM context. Hashes are deterministic — the same user always maps to the same hash, so the model can still distinguish between users in group chats; routing and delivery use the original values internally.

## Code Execution

Configure the `execute_code` tool:

```yaml
code_execution:
  mode: project                # project (default) | strict
  timeout: 300                 # Max execution time in seconds
  max_tool_calls: 50           # Max tool calls within code execution
```

`mode` controls the working directory and Python interpreter for scripts:

- **`project`** (default) — scripts run in the session's working directory with the active virtualenv/conda env's python. Project deps (`pandas`, `torch`, project packages) and relative paths (`.env`, `./data.csv`) resolve naturally, matching what `terminal()` sees.
- **`strict`** — scripts run in a temp staging directory with `sys.executable` (Hermes's own python). Maximum reproducibility, but project deps and relative paths won't resolve.

Environment scrubbing (strips `*_API_KEY`, `*_TOKEN`, `*_SECRET`, `*_PASSWORD`, `*_CREDENTIAL`, `*_PASSWD`, `*_AUTH`) and the tool whitelist apply identically in both modes — switching mode does not change the security posture.

## Security

Pre-execution security scanning and secret redaction:

```yaml
security:
  redact_secrets: true           # Redact API key patterns in tool output and logs (on by default)
  tirith_enabled: true           # Enable Tirith security scanning for terminal commands
  tirith_path: "tirith"          # Path to tirith binary (default: "tirith" in $PATH)
  tirith_timeout: 5              # Seconds to wait for tirith scan before timing out
  tirith_fail_open: true         # Allow command execution if tirith is unavailable
  website_blocklist:             # See Website Blocklist section below
    enabled: false
    domains: []
    shared_files: []
```

- `redact_secrets` — when `true`, automatically detects and redacts patterns that look like API keys, tokens, and passwords in tool output before it enters the conversation context and logs. **On by default**. Set to `false` explicitly only when you need raw credential-like strings for debugging or redactor development.
- `tirith_enabled` — when `true`, terminal commands are scanned by Tirith before execution to detect potentially dangerous operations.
- `tirith_path` — path to the tirith binary. Set this if tirith is installed in a non-standard location.
- `tirith_timeout` — maximum seconds to wait for a tirith scan. Commands proceed if the scan times out.
- `tirith_fail_open` — when `true` (default), commands are allowed to execute if tirith is unavailable or fails. Set to `false` to block commands when tirith cannot verify them.

## Website Blocklist

Block specific domains from being accessed by the agent's web and browser tools:

```yaml
security:
  website_blocklist:
    enabled: false               # Enable URL blocking (default: false)
    domains:                     # List of blocked domain patterns
      - "*.internal.company.com"
      - "admin.example.com"
      - "*.local"
    shared_files:                # Load additional rules from external files
      - "/etc/hermes/blocked-sites.txt"
```

When enabled, any URL matching a blocked domain pattern is rejected before the web or browser tool executes. This applies to `web_search`, `web_extract`, `browser_navigate`, and any tool that accesses URLs. Domain rules support exact domains (`admin.example.com`), wildcard subdomains (`*.internal.company.com`, blocks all subdomains), and TLD wildcards (`*.local`). Shared files contain one domain rule per line (blank lines and `#` comments ignored); missing or unreadable files log a warning but don't disable other web tools. The policy is cached for 30 seconds, so config changes take effect quickly without restart.

## Smart Approvals

Control how Hermes handles potentially dangerous commands via `approvals.mode` (`manual` | `smart` | `off`):

| Mode | Behavior |
|------|----------|
| `manual` (default) | Prompt the user before executing any flagged command. In the CLI, shows an interactive approval dialog. In messaging, queues a pending approval request. |
| `smart` | Use an auxiliary LLM to assess whether a flagged command is actually dangerous. Low-risk commands are auto-approved with session-level persistence. Genuinely risky commands are escalated to the user. |
| `off` | Skip all approval checks. Equivalent to `HERMES_YOLO_MODE=true`. **Use with caution.** |

Smart mode is particularly useful for reducing approval fatigue — it lets the agent work more autonomously on safe operations while still catching genuinely destructive commands. Setting `approvals.mode: off` disables all safety checks for terminal commands; only use this in trusted, sandboxed environments.

## Checkpoints

Automatic filesystem snapshots before destructive file operations, configured under the `checkpoints` block (also enabled via `hermes chat --checkpoints`): `checkpoints.enabled` (default `false`, opt-in) toggles automatic checkpoints, and `checkpoints.max_snapshots` (default `20`) caps how many checkpoints are kept per directory.

## Delegation

Configure subagent behavior for the delegate tool:

```yaml
delegation:
  max_concurrent_children: 3                # Parallel children per batch (floor 1, no ceiling). Also via DELEGATION_MAX_CONCURRENT_CHILDREN env var.
  max_spawn_depth: 1                        # Delegation tree depth cap (1-3, clamped). 1 = flat (default): parent spawns leaves that cannot delegate.
  orchestrator_enabled: true                # Global kill switch. When false, role="orchestrator" is ignored and every child is forced to leaf regardless of max_spawn_depth.
```

By default subagents inherit the parent agent's provider and model. Set `delegation.provider` and `delegation.model` to route subagents to a different provider:model pair (e.g., a cheap/fast model for narrow subtasks). A direct-endpoint path is also available via `delegation.base_url` / `delegation.api_key` / `delegation.model`, which takes precedence over `delegation.provider`; if `api_key` is omitted Hermes falls back to `OPENAI_API_KEY`. `delegation.api_mode` (`chat_completions` | `codex_responses` | `anthropic_messages`) is auto-detected from `base_url` but can be set explicitly for endpoints the heuristic can't classify (Azure AI Foundry, MiniMax, Zhipu GLM, LiteLLM proxies).

**Width and depth:** `max_concurrent_children` caps parallel subagents per batch (default `3`, floor 1, no ceiling); when the model submits more tasks than the cap, `delegate_task` returns a tool error rather than silently truncating. `max_spawn_depth` controls tree depth (clamped 1-3): at the default `1` delegation is flat (children cannot spawn grandchildren and `role="orchestrator"` degrades to `leaf`), `2` lets orchestrator children spawn leaf grandchildren, `3` allows three-level trees. `orchestrator_enabled: false` forces every child back to leaf. Cost scales multiplicatively — at `max_spawn_depth: 3` with `max_concurrent_children: 3` the tree can reach 3×3×3 = 27 concurrent leaf agents.

## Clarify

Configure the clarification prompt behavior with `clarify.timeout` (default `120`) — the seconds to wait for a user clarification response.

## Context Files (SOUL.md, AGENTS.md)

Hermes uses two different context scopes:

| File | Purpose | Scope |
|------|---------|-------|
| `SOUL.md` | **Primary agent identity** — defines who the agent is (slot #1 in the system prompt) | `~/.hermes/SOUL.md` or `$HERMES_HOME/SOUL.md` |
| `.hermes.md` / `HERMES.md` | Project-specific instructions (highest priority) | Walks to git root |
| `AGENTS.md` | Project-specific instructions, coding conventions | Recursive directory walk |
| `CLAUDE.md` | Claude Code context files (also detected) | Working directory only |
| `.cursorrules` | Cursor IDE rules (also detected) | Working directory only |
| `.cursor/rules/*.mdc` | Cursor rule files (also detected) | Working directory only |

- **SOUL.md** is the agent's primary identity. It occupies slot #1 in the system prompt, completely replacing the built-in default identity. Edit it to fully customize who the agent is. If SOUL.md is missing, empty, or cannot be loaded, Hermes falls back to a built-in default identity, and Hermes automatically seeds a default `SOUL.md` if one does not exist.
- **Project context files use a priority system** — only ONE type is loaded (first match wins): `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`. SOUL.md is always loaded independently.
- **AGENTS.md** is hierarchical: if subdirectories also have AGENTS.md, all are combined.
- All loaded context files are capped at `context_file_max_chars` characters (default 20,000) with smart truncation.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md` · https://hermes-agent.nousresearch.com/docs/user-guide/configuration
**Last Updated**: 2026-06-19
**Status**: Active
