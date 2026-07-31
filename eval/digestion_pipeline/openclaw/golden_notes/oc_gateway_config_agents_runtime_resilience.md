---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - agent_defaults
keywords:
  - openclaw agents defaults heartbeat
  - openclaw compaction config
  - agents.defaults.runRetries
  - openclaw contextpruning cache-ttl
  - block streaming config
  - typing indicators openclaw
  - agents.defaults.sandbox docker ssh openshell
  - openclaw sandbox backend
  - runtime resilience config
topics:
  - OpenClaw
  - Agent Defaults Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-agents
access_control_group: ["general"]
---

# OpenClaw — Agent Defaults: Runtime Resilience and Sandbox Configuration

## Overview

This note documents the runtime-resilience and presentation configuration keys under `agents.defaults.*` on the OpenClaw gateway `config-agents` reference page. It covers the periodic `heartbeat` runs, the `compaction` block (history summarization), the `runRetries` outer-loop iteration boundaries, `contextPruning` (in-memory tool-result pruning), `Block streaming`, `Typing indicators`, and the large `sandbox` execution-policy block (Docker / SSH / OpenShell backends, browser sandboxing, workspace access, scope, and pruning). These are the agent-defaults knobs that keep a long-running agent live, bounded, and isolated; every config key, default, and value list below is copied verbatim from the mirror at `inbox/openclaw_docs/gateway/config-agents.md`.

## `agents.defaults.heartbeat`

Periodic heartbeat runs. Heartbeats run full agent turns, so shorter intervals burn more tokens.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // 0m disables
        model: "openai/gpt-5.4-mini",
        includeReasoning: false,
        includeSystemPromptSection: true,
        lightContext: false,
        isolatedSession: false,
        skipWhenBusy: false,
        session: "main",
        to: "+15555550123",
        directPolicy: "allow", // allow (default) | block
        target: "none",
        prompt: "Read HEARTBEAT.md if it exists...",
        ackMaxChars: 300,
        suppressToolErrorWarnings: false,
        timeoutSeconds: 45,
      },
    },
  },
}
```

- `every`: duration string (ms/s/m/h). Default: `30m` (API-key auth) or `1h` (OAuth auth). Set to `0m` to disable.
- `includeSystemPromptSection`: when false, omits the Heartbeat section from the system prompt and skips `HEARTBEAT.md` injection into bootstrap context. Default: `true`.
- `suppressToolErrorWarnings`: when true, suppresses tool error warning payloads during heartbeat runs.
- `timeoutSeconds`: maximum time in seconds allowed for a heartbeat agent turn before it is aborted. Leave unset to use `agents.defaults.timeoutSeconds` when set, otherwise the heartbeat cadence capped at 600 seconds.
- `directPolicy`: direct/DM delivery policy. `allow` (default) permits direct-target delivery. `block` suppresses direct-target delivery and emits `reason=dm-blocked`.
- `lightContext`: when true, heartbeat runs use lightweight bootstrap context and keep only `HEARTBEAT.md` from workspace bootstrap files.
- `isolatedSession`: when true, each heartbeat runs in a fresh session with no prior conversation history. Same isolation pattern as cron `sessionTarget: "isolated"`. Reduces per-heartbeat token cost from ~100K to ~2-5K tokens.
- `skipWhenBusy`: when true, heartbeat runs defer on that agent's extra busy lanes (its own session-keyed subagent or nested command work). Cron lanes always defer heartbeats, even without this flag.
- Per-agent: set `agents.list[].heartbeat`. When any agent defines `heartbeat`, only those agents run heartbeats.

## `agents.defaults.compaction`

Controls history summarization for long sessions; `mode` is `default` or `safeguard` (chunked summarization for long histories).

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard", // default | safeguard
        provider: "my-provider",
        timeoutSeconds: 180,
        reserveTokensFloor: 24000,
        keepRecentTokens: 50000,
        identifierPolicy: "strict", // strict | off | custom
        qualityGuard: { enabled: true, maxRetries: 1 },
        midTurnPrecheck: { enabled: false },
        postCompactionSections: ["Session Startup", "Red Lines"],
        model: "openrouter/anthropic/claude-sonnet-4-6",
        truncateAfterCompaction: true,
        maxActiveTranscriptBytes: "20mb",
        notifyUser: true,
        memoryFlush: { enabled: true, softThresholdTokens: 6000 },
      },
    },
  },
}
```

- `provider`: id of a registered compaction provider plugin. When set, the provider's `summarize()` is called instead of built-in LLM summarization. Falls back to built-in on failure. Setting a provider forces `mode: "safeguard"`.
- `timeoutSeconds`: maximum seconds allowed for a single compaction operation before OpenClaw aborts it. Default: `180`.
- `keepRecentTokens`: agent cut-point budget for keeping the most recent transcript tail verbatim. Manual `/compact` honors this when explicitly set; otherwise manual compaction is a hard checkpoint.
- `identifierPolicy`: `strict` (default), `off`, or `custom`. `strict` prepends built-in opaque identifier retention guidance during compaction summarization. `identifierInstructions` provides optional custom identifier-preservation text used when `identifierPolicy=custom`.
- `qualityGuard`: retry-on-malformed-output checks for safeguard summaries. Enabled by default in safeguard mode; set `enabled: false` to skip the audit.
- `midTurnPrecheck`: optional tool-loop pressure check. When `enabled: true`, OpenClaw checks context pressure after tool results are appended and before the next model call; if context no longer fits, it aborts the current attempt before submitting the prompt. Works with both `default` and `safeguard` modes. Default: disabled.
- `postCompactionSections`: optional AGENTS.md H2/H3 section names to re-inject after compaction. Reinjection is disabled when unset or set to `[]`.
- `model`: optional `provider/model-id` or bare alias from `agents.defaults.models` for compaction summarization only. When unset, compaction uses the session's primary model.
- `maxActiveTranscriptBytes`: optional byte threshold (`number` or strings like `"20mb"`) that triggers normal local compaction before a run when the active JSONL grows past the threshold. Requires `truncateAfterCompaction` so successful compaction can rotate to a smaller successor transcript. Disabled when unset or `0`.
- `notifyUser`: when `true`, sends brief notices when compaction starts and completes. Disabled by default to keep compaction silent.
- `memoryFlush`: silent agentic turn before auto-compaction to store durable memories. Skipped when workspace is read-only.

## `agents.defaults.runRetries`

Outer run-loop retry iteration boundaries for the embedded agent runtime, preventing infinite execution loops during failure recovery. This setting currently only applies to the embedded agent runtime, not ACP or CLI runtimes.

```json5
{
  agents: {
    defaults: {
      runRetries: { base: 24, perProfile: 8, min: 32, max: 160 },
    },
    list: [
      { id: "main", runRetries: { max: 50 } }, // optional per-agent overrides
    ],
  },
}
```

- `base`: base number of run retry iterations for the outer run loop. Default: `24`.
- `perProfile`: additional run retry iterations granted per fallback profile candidate. Default: `8`.
- `min`: minimum absolute limit for run retry iterations. Default: `32`.
- `max`: maximum absolute limit for run retry iterations to prevent runaway execution. Default: `160`.

## `agents.defaults.contextPruning`

Prunes old tool results from in-memory context before sending to the LLM. Does not modify session history on disk.

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl", // off | cache-ttl
        ttl: "1h",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

`cache-ttl` mode behavior: `mode: "cache-ttl"` enables pruning passes; `ttl` controls how often pruning can run again (after the last cache touch). Pruning soft-trims oversized tool results first, then hard-clears older tool results if needed. `softTrimRatio` and `hardClearRatio` accept values from `0.0` through `1.0`; config validation rejects values outside that range. Soft-trim keeps beginning + end and inserts `...` in the middle; hard-clear replaces the entire tool result with the placeholder. Image blocks are never trimmed/cleared, ratios are character-based (approximate) not exact token counts, and if fewer than `keepLastAssistants` assistant messages exist, pruning is skipped.

## Block streaming

Controls how partial assistant replies are streamed as discrete blocks.

```json5
{
  agents: {
    defaults: {
      blockStreamingDefault: "off", // on | off
      blockStreamingBreak: "text_end", // text_end | message_end
      blockStreamingChunk: { minChars: 800, maxChars: 1200 },
      blockStreamingCoalesce: { idleMs: 1000 },
      humanDelay: { mode: "natural" }, // off | natural | custom (use minMs/maxMs)
    },
  },
}
```

- Non-Telegram channels require explicit `*.blockStreaming: true` to enable block replies.
- Channel overrides: `channels.<channel>.blockStreamingCoalesce` (and per-account variants). Signal/Slack/Discord/Google Chat default `minChars: 1500`.
- `humanDelay`: randomized pause between block replies. `natural` = 800–2500ms. Per-agent override: `agents.list[].humanDelay`.

## Typing indicators

Set under `agents.defaults`: `typingMode` (values `never | instant | thinking | message`) and `typingIntervalSeconds: 6`. Defaults are `instant` for direct chats/mentions and `message` for unmentioned group chats. Per-session overrides: `session.typingMode`, `session.typingIntervalSeconds`.

## `agents.defaults.sandbox`

Optional sandboxing for the embedded agent. The block selects a backend (`docker`, `ssh`, or `openshell`), a `scope`, a `workspaceAccess` level, and per-backend settings.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        backend: "docker", // docker | ssh | openshell
        scope: "agent", // session | agent | shared
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          readOnlyRoot: true,
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          memory: "1g",
        },
        ssh: { target: "user@gateway-host:22", command: "ssh" },
        browser: { enabled: false, cdpPort: 9222, vncPort: 5900, noVncPort: 6080 },
        prune: { idleHours: 24, maxAgeDays: 7 },
      },
    },
  },
}
```

### Backend

- `docker`: local Docker runtime (default).
- `ssh`: generic SSH-backed remote runtime.
- `openshell`: OpenShell runtime. When `backend: "openshell"` is selected, runtime-specific settings move to `plugins.entries.openshell.config`.

### Workspace access and scope

Workspace access: `none` gives a per-scope sandbox workspace under `~/.openclaw/sandboxes`; `ro` mounts the sandbox workspace at `/workspace` with the agent workspace mounted read-only at `/agent`; `rw` mounts the agent workspace read/write at `/workspace`. Scope: `session` = per-session container + workspace; `agent` = one container + workspace per agent (default); `shared` = shared container and workspace (no cross-session isolation).

### SSH backend

SSH backend config: `target` (SSH target in `user@host[:port]` form), `command` (SSH client command, default `ssh`), `workspaceRoot` (absolute remote root used for per-scope workspaces), `identityFile`/`certificateFile`/`knownHostsFile` (existing local files passed to OpenSSH), `identityData`/`certificateData`/`knownHostsData` (inline contents or SecretRefs that OpenClaw materializes into temp files at runtime), and `strictHostKeyChecking`/`updateHostKeys` (OpenSSH host-key policy knobs). SSH auth precedence: `identityData` wins over `identityFile`, `certificateData` wins over `certificateFile`, and `knownHostsData` wins over `knownHostsFile`; SecretRef-backed `*Data` values are resolved from the active secrets runtime snapshot before the sandbox session starts. SSH backend behavior: seeds the remote workspace once after create or recreate, then keeps the remote SSH workspace canonical, routes `exec`, file tools, and media paths over SSH, does not sync remote changes back to the host automatically, and does not support sandbox browser containers.

### Docker network, setup, and browser

`setupCommand` runs once after container creation (via `sh -lc`) and needs network egress, writable root, and root user. Containers default to `network: "none"` — set to `"bridge"` (or a custom bridge network) if the agent needs outbound access; `"host"` is blocked, and `"container:<id>"` is blocked by default unless you explicitly set `sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true` (break-glass). Inbound attachments are staged into `media/inbound/*` in the active workspace, and `docker.binds` mounts additional host directories (global and per-agent binds are merged). Sandboxed browser (`sandbox.browser.enabled`) runs Chromium + CDP in a container with a noVNC URL injected into the system prompt and does not require `browser.enabled` in `openclaw.json`; `allowHostControl: false` (default) blocks sandboxed sessions from targeting the host browser, `network` defaults to `openclaw-sandbox-browser` (dedicated bridge network), and `cdpSourceRange` optionally restricts CDP ingress at the container edge to a CIDR range. Browser sandboxing and `sandbox.docker.binds` are Docker-only.

### Sandbox tool allow/deny

The companion `tools.sandbox.tools` block sets the allow/deny tool sets for sandboxed runs. The source `allow` set is `["exec", "process", "read", "write", "edit", "apply_patch", "sessions_list", "sessions_history", "sessions_send", "sessions_spawn", "session_status"]` and the `deny` set is `["browser", "canvas", "nodes", "cron", "discord", "gateway"]`.

OpenShell mode: `mirror` seeds remote from local before exec and syncs back after exec (local workspace stays canonical); `remote` seeds remote once when the sandbox is created, then keeps the remote workspace canonical (host-local edits made outside OpenClaw are not synced into the sandbox automatically after the seed step).

**Source**: OpenClaw documentation — `gateway/config-agents` (mirror `inbox/openclaw_docs/gateway/config-agents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
