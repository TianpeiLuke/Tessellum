---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - tools_policy
keywords:
  - openclaw tools config
  - tool profiles minimal coding messaging full
  - tool groups group runtime group fs
  - sandbox tool policy bundle-mcp
  - tools allow deny deny wins
  - tools byProvider toolsBySender elevated
  - tools loopDetection exec media
  - agents defaults subagents sessions_spawn
topics:
  - OpenClaw
  - Gateway Tools Policy
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-tools
access_control_group: ["general"]
---

# OpenClaw — Gateway `tools.*` Policy and Sandbox Tool Gating

## Overview

This note is the procedure for configuring the OpenClaw `tools.*` policy surface — the keys under the `## Tools` section of the `gateway/config-tools` page that decide which tools the agent can call. It covers tool profiles (the base allowlist), tool groups, the additional sandbox tool gate for MCP/plugin tools (`bundle-mcp`), `tools.codeMode`, `tools.allow`/`tools.deny` (deny wins), and the per-tool keys `byProvider`, `toolsBySender`, `elevated`, `exec`, `loopDetection`, `web`, `media`, `agentToAgent`, `sessions`, `sessions_spawn`, `experimental`, plus `agents.defaults.subagents`. The companion `models.providers.*` custom-provider half of the same source page is digested separately (see Related Notes). All keys and defaults below are copied verbatim from the source page.

## Tool profiles

`tools.profile` sets a base allowlist that is applied *before* `tools.allow`/`tools.deny`. Local onboarding defaults new local configs to `tools.profile: "coding"` when unset (existing explicit profiles are preserved). The four profiles:

| Profile | Includes |
| --- | --- |
| `minimal` | `session_status` only |
| `coding` | `group:fs`, `group:runtime`, `group:web`, `group:sessions`, `group:memory`, `cron`, `image`, `image_generate`, `skill_workshop`, `video_generate` |
| `messaging` | `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status` |
| `full` | No restriction (same as unset) |

## Tool groups

Tool groups expand into the concrete tool ids that profiles and allow/deny lists reference:

| Group | Tools |
| --- | --- |
| `group:runtime` | `exec`, `process`, `code_execution` (`bash` is accepted as an alias for `exec`) |
| `group:fs` | `read`, `write`, `edit`, `apply_patch` |
| `group:sessions` | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `subagents`, `session_status` |
| `group:memory` | `memory_search`, `memory_get` |
| `group:web` | `web_search`, `x_search`, `web_fetch` |
| `group:ui` | `browser`, `canvas` |
| `group:automation` | `heartbeat_respond`, `cron`, `gateway` |
| `group:messaging` | `message` |
| `group:nodes` | `nodes` |
| `group:agents` | `agents_list`, `update_plan` |
| `group:media` | `image`, `image_generate`, `music_generate`, `video_generate`, `tts` |
| `group:openclaw` | All built-in tools (excludes provider plugins) |
| `group:plugins` | Tools owned by loaded plugins, including configured MCP servers exposed through `bundle-mcp` |

## MCP and plugin tools inside sandbox tool policy

Configured MCP servers are exposed as plugin-owned tools under the `bundle-mcp` plugin id. Normal tool profiles can allow them, but `tools.sandbox.tools` is an *additional* gate for sandboxed sessions. If sandbox mode is `"all"` or `"non-main"`, include one of these entries in the sandbox tool allowlist when MCP/plugin tools should be visible: `bundle-mcp` for OpenClaw-managed MCP servers from `mcp.servers`; the plugin id for a specific native plugin; `group:plugins` for all loaded plugin-owned tools; or exact MCP server tool names or server globs such as `outlook__send_mail` or `outlook__*` when you only want one server. Server globs use the provider-safe MCP server prefix, not necessarily the raw `mcp.servers` key — non-`[A-Za-z0-9_-]` characters become `-`, names that do not start with a letter get an `mcp-` prefix, and long or duplicate prefixes may be truncated or suffixed (for example, `mcp.servers["Outlook Graph"]` uses a glob like `outlook-graph__*`).

```json5
{
  agents: { defaults: { sandbox: { mode: "all" } } },
  mcp: {
    servers: {
      outlook: { command: "node", args: ["./outlook-mcp.js"] },
    },
  },
  tools: {
    sandbox: {
      tools: {
        alsoAllow: ["web_search", "web_fetch", "memory_search", "memory_get", "bundle-mcp"],
      },
    },
  },
}
```

Without that sandbox-layer entry, the MCP server can still load successfully while its tools are filtered before the provider request. Use `openclaw doctor` to catch this shape for OpenClaw-managed servers in `mcp.servers`. MCP servers loaded from bundled plugin manifests or Claude `.mcp.json` use the same sandbox gate, but this diagnostic does not enumerate those sources yet; use the same allowlist entries if their tools disappear in sandboxed turns.

## `tools.codeMode`

`tools.codeMode` enables the generic OpenClaw code-mode surface. When enabled for a run with tools, the model sees only `exec` and `wait`; normal OpenClaw tools move behind the in-sandbox `tools.*` catalog bridge, and MCP tools are available through the generated `MCP` namespace. Set `tools.codeMode.enabled: true`, or use the shorthand `tools.codeMode: true`. MCP declarations are exposed through the read-only virtual API file surface in code mode: guest code can call `API.list("mcp")` and `API.read("mcp/<server>.d.ts")` to inspect TypeScript-style signatures before calling `MCP.<server>.<tool>()` (see the source page's `reference/code-mode` link for the runtime contract, limits, and debugging steps).

## `tools.allow` / `tools.deny`

Global tool allow/deny policy where **deny wins**. Matching is case-insensitive and supports `*` wildcards, and the policy is applied even when the Docker sandbox is off. `write` and `apply_patch` are separate tool ids: `allow: ["write"]` also enables `apply_patch` for compatible models, but `deny: ["write"]` does *not* deny `apply_patch`. To block all file mutation, deny `group:fs` or list each mutating tool explicitly (`deny: ["write", "edit", "apply_patch"]`).

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

## `tools.byProvider` and `tools.toolsBySender`

`tools.byProvider` further restricts tools for specific providers or models, applied in the order base profile → provider profile → allow/deny. `tools.toolsBySender` restricts tools for a specific requester identity; it is defense-in-depth on top of channel access control, and sender values must come from the channel adapter, not message text. `toolsBySender` keys use explicit prefixes — `channel:<channelId>:<senderId>`, `id:<senderId>`, `e164:<phone>`, `username:<handle>`, `name:<displayName>`, or `"*"`. Channel ids are canonical OpenClaw ids (aliases such as `teams` normalize to `msteams`); legacy unprefixed keys are accepted as `id:` only; matching order is channel+id, id, e164, username, name, then wildcard. Per-agent `agents.list[].tools.toolsBySender` overrides the global sender match when it matches, even with an empty `{}` policy.

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
      "openai/gpt-5.4": { allow: ["group:fs", "sessions_list"] },
    },
    toolsBySender: {
      "channel:discord:1234567890123": { alsoAllow: ["group:fs"] },
      "id:guest-user-id": { deny: ["group:runtime", "group:fs"] },
      "*": { deny: ["exec", "process", "write", "edit", "apply_patch"] },
    },
  },
}
```

## `tools.elevated`

`tools.elevated` controls elevated exec access *outside* the sandbox via `enabled` plus an `allowFrom` map of channel → identifiers (e.g. `whatsapp`, `discord`). A per-agent override (`agents.list[].tools.elevated`) can only further restrict. The `/elevated on|off|ask|full` command stores state per session, and inline directives apply to a single message. Elevated `exec` bypasses sandboxing and uses the configured escape path (`gateway` by default, or `node` when the exec target is `node`).

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["1234567890123", "987654321098765432"],
      },
    },
  },
}
```

## `tools.exec`

`tools.exec` configures the exec/process tool runtime. Fields include `backgroundMs`, `timeoutSec`, `cleanupMs`, `notifyOnExit`, `notifyOnExitEmptySuccess`, `commandHighlighting`, and an `applyPatch` sub-object (`enabled`, `allowModels`). Example values from the source: `backgroundMs: 10000`, `timeoutSec: 1800`, `cleanupMs: 1800000`, `notifyOnExit: true`, `notifyOnExitEmptySuccess: false`, `commandHighlighting: false`, `applyPatch: { enabled: false, allowModels: ["gpt-5.5"] }`.

## `tools.loopDetection`

Tool-loop safety checks are **disabled by default**; set `enabled: true` to activate detection. Settings can be defined globally in `tools.loopDetection` and overridden per-agent at `agents.list[].tools.loopDetection`. Fields: `historySize` (max tool-call history retained for loop analysis), `warningThreshold` (repeating no-progress pattern threshold for warnings), `criticalThreshold` (higher repeating threshold for blocking critical loops), `globalCircuitBreakerThreshold` (hard stop threshold for any no-progress run), and the `detectors` toggles — `genericRepeat` (warn on repeated same-tool/same-args calls), `knownPollNoProgress` (warn/block on known poll tools such as `process.poll`, `command_status`), and `pingPong` (warn/block on alternating no-progress pair patterns). Validation fails if `warningThreshold >= criticalThreshold` or `criticalThreshold >= globalCircuitBreakerThreshold`.

```json5
{
  tools: {
    loopDetection: {
      enabled: true,
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

## `tools.web`

`tools.web` configures the built-in web tools. Under `search`: `enabled`, `apiKey` (e.g. `"brave_api_key"`, or the `BRAVE_API_KEY` env var), `maxResults` (e.g. `5`), `timeoutSeconds` (`30`), `cacheTtlMinutes` (`15`). Under `fetch`: `enabled`, `provider` (optional, e.g. `"firecrawl"`; omit for auto-detect), `maxChars` (`50000`), `maxCharsCap` (`50000`), `maxResponseBytes` (`2000000`), `timeoutSeconds` (`30`), `cacheTtlMinutes` (`15`), `maxRedirects` (`3`), `readability` (`true`), and `userAgent` (e.g. `"custom-ua"`).

## `tools.media`

`tools.media` configures inbound media understanding (image/audio/video) with a top-level `concurrency` and an `asyncCompletion.directSend` flag (deprecated — completions stay agent-mediated). Each of `audio`, `image`, and `video` has `enabled`, optional `maxBytes`, optional per-modality `scope` (a `default` action plus `rules` matching on fields such as `chatType`), `timeoutSeconds`, and a `models` list. A media model entry is either a **provider entry** (`type: "provider"` or omitted) with `provider` (e.g. `openai`, `anthropic`, `google`/`gemini`, `groq`), `model`, and `profile`/`preferredProfile` for `auth-profiles.json` selection, or a **CLI entry** (`type: "cli"`) with `command` and templated `args` (supporting `{{MediaPath}}`, `{{Prompt}}`, `{{MaxChars}}`; `openclaw doctor --fix` migrates deprecated `{input}` placeholders to `{{MediaPath}}`). Common fields include `capabilities` (`image`/`audio`/`video`; defaults: `openai`/`anthropic`/`minimax` → image, `google` → image+audio+video, `groq` → audio), plus per-entry `prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language`. Failures fall back to the next entry, and provider auth follows the order `auth-profiles.json` → env vars → `models.providers.*.apiKey`.

## `tools.agentToAgent`

`tools.agentToAgent` gates the agent-to-agent tool with `enabled` (default `false`) and an `allow` list of target agent ids (e.g. `["home", "work"]`).

## `tools.sessions` and `tools.sessions_spawn`

`tools.sessions` controls which sessions can be targeted by the session tools (`sessions_list`, `sessions_history`, `sessions_send`) via `visibility`, default `tree` (the current session plus sessions spawned by it, such as subagents). The visibility scopes are: `self` (only the current session key), `tree` (current session + spawned sessions), `agent` (any session belonging to the current agent id — can include other users if you run per-sender sessions under the same agent id), and `all` (any session; cross-agent targeting still requires `tools.agentToAgent`). A sandbox clamp forces `tree` even when `visibility="all"` if the current session is sandboxed and `agents.defaults.sandbox.sessionToolsVisibility="spawned"`. When visibility is not `all`, `sessions_list` includes a compact `visibility` field describing the effective mode and a warning that some sessions may be omitted.

`tools.sessions_spawn` controls inline attachment support for `sessions_spawn` via an `attachments` block: `enabled` (opt-in; default `false`), `maxTotalBytes` (e.g. `5242880` = 5 MB total), `maxFiles` (e.g. `50`), `maxFileBytes` (e.g. `1048576` = 1 MB per file), and `retainOnSessionKeep` (keep attachments when `cleanup="keep"`). Subagent attachments are materialized into the child workspace at `.openclaw/attachments/<uuid>/` with a `.manifest.json`; ACP attachments are image-only and forwarded inline after the same file-count/per-file-byte/total-byte limits pass; attachment content is automatically redacted from transcript persistence; Base64 inputs are validated with strict alphabet/padding checks and a pre-decode size guard; subagent attachment permissions are `0700` for directories and `0600` for files; and subagent cleanup follows the `cleanup` policy (`delete` always removes attachments, `keep` retains them only when `retainOnSessionKeep: true`).

## `tools.experimental`

`tools.experimental` holds experimental built-in tool flags, default off unless a strict-agentic GPT-5 auto-enable rule applies. `planTool` enables the structured `update_plan` tool for non-trivial multi-step work tracking. Its default is `false` unless `agents.defaults.embeddedAgent.executionContract` (or a per-agent override) is set to `"strict-agentic"` for an OpenAI or OpenAI Codex GPT-5-family run; set `true` to force the tool on outside that scope, or `false` to keep it off even for strict-agentic GPT-5 runs. When enabled, the system prompt also adds usage guidance so the model only uses it for substantial work and keeps at most one step `in_progress`.

## `agents.defaults.subagents`

`agents.defaults.subagents` sets defaults for spawned sub-agents: `model` (default model for spawned sub-agents; if omitted, sub-agents inherit the caller's model); `allowAgents` (default allowlist of configured target agent ids for `sessions_spawn` when the requester agent does not set its own `subagents.allowAgents` — `["*"]` = any configured target, default same agent only; stale entries whose agent config was deleted are rejected by `sessions_spawn` and omitted from `agents_list`, run `openclaw doctor --fix` to clean them up); `maxConcurrent`; `runTimeoutSeconds` (default timeout in seconds for `sessions_spawn`, `0` means no timeout); `announceTimeoutMs` (per-call timeout in milliseconds for gateway `agent` announce delivery attempts, default `120000` — transient retries can make the total announce wait longer than one configured timeout); and `archiveAfterMinutes`. Per-subagent tool policy is set via `tools.subagents.tools.allow` / `tools.subagents.tools.deny`.

## Related Notes

**Terms**

- **[MCP](../../term_dictionary/term_mcp.md)** — Model Context Protocol server/tool standard; relevance: configured MCP servers are exposed as `bundle-mcp` plugin tools gated by `tools.sandbox.tools`.
- **[MCP Gateway](../../term_dictionary/term_mcp_gateway.md)** — fronts MCP servers as managed tools; relevance: `mcp.servers` entries surface through the same sandbox tool gate this note documents.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolated execution mode; relevance: `sandbox.mode` all/non-main is the gate that makes `tools.sandbox.tools.alsoAllow` load-bearing.
- **[Function Calling](../../term_dictionary/term_function_calling.md)** — model tool-invocation; relevance: `tools.*` allow/deny defines the callable tool surface the model sees.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — registered tool catalog; relevance: tool profiles (minimal/coding/messaging/full) and groups define the registered set this policy filters.
- **[Subagent](../../term_dictionary/term_subagent.md)** — spawned child agent; relevance: `tools.sessions_spawn` and `agents.defaults.subagents` are config keys covered here.
- **[Multi-Agent](../../term_dictionary/term_multi_agent.md)** — agent-to-agent orchestration; relevance: `tools.agentToAgent` enables the agent-to-agent tool this policy governs.
- **[Deny-First](../../term_dictionary/term_deny_first.md)** — deny-wins authorization default; relevance: `tools.deny` wins over `tools.allow` — the exact deny-first semantics this note states.
- **[Code Execution Tool](../../term_dictionary/term_code_execution_tool.md)** — sandboxed code-run tool; relevance: `group:runtime` (`exec`/`process`/`code_execution`) is the highest-risk tool group gated here.
- **[Access Control](../../term_dictionary/term_access_control.md)** — authorization policy; relevance: `byProvider`/`toolsBySender`/`elevated` are the per-sender authorization layers documented.

**Docs**

- **[Claude Code — Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md)** — how sandbox and permission layers compose; relevance: the same two-layer model (sandbox gate + tool allowlist) OpenClaw applies.
- **[Claude Code — Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md)** — per-tool allow/deny rule syntax; relevance: direct analog to `tools.allow`/`tools.deny` wildcard/case-insensitive rules.
- **[Claude Code — Permission System and Rules](../claude_code/cc_permission_system_and_rules.md)** — allow/ask/deny precedence; relevance: parallels OpenClaw's deny-wins precedence over profile/group baselines.
- **[Claude Code — Execution Tool Behavior](../claude_code/cc_execution_tool_behavior.md)** — bash/exec tool runtime semantics; relevance: documents the `exec`/`code_execution` tool this note's `group:runtime` and `tools.exec` gate.
- **[Claude Code — MCP Installation Scopes](../claude_code/cc_mcp_installation_scopes.md)** — where MCP servers register; relevance: scope analog to OpenClaw's `bundle-mcp`/server-glob sandbox allowlist entries.
- **[Hermes — Tools Runtime](../hermes_agent/hermes_tools_runtime.md)** — tool registry + lazy-load runtime; relevance: implementation view of the registered tool set OpenClaw's profiles/groups select from.
- **[Hermes — MCP Concept and Config](../hermes_agent/hermes_mcp_concept_config.md)** — MCP server config model; relevance: the server-config shape that becomes plugin-owned tools under the sandbox gate.
- **[oc_gateway_config_custom_providers](oc_gateway_config_custom_providers.md)** — companion half of config-tools.md (planned, this series); relevance: the other tool-adjacent surface (`models.providers.*`) from the same source page.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — Tools-and-custom-providers field reference (planned, this series); relevance: the field-level map of every `tools.*` key summarized here.
- **[oc_gateway_configuration_overview](oc_gateway_configuration_overview.md)** — parent config overview (planned, this series); relevance: where the `tools.*` block fits in the whole config tree.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: implements the `tools.*` policy + sandbox tool gating.
- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: applies the tool profile/group/allowlist to the agent's callable set.
- **[repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md)** — skills layer; relevance: `skill_workshop` is in the coding profile this note lists.

**Snippets**

- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool allow/deny policy resolution; relevance: the exact deny-wins/profile-baseline logic this note documents.
- **[snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md)** — registered tool catalog assembly; relevance: how profiles/groups expand into the concrete tool set.
- **[snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md)** — deny-list for dangerous tools; relevance: code-side of `group:fs`/`group:runtime` deny enforcement.
- **[snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md)** — exec/filesystem gating; relevance: `tools.exec` + `group:fs` enforcement implementation.
- **[snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md)** — runtime exec audit; relevance: how elevated/exec tool use is audited under policy.
- **[snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md)** — node command policy; relevance: the gateway-side command-gating analog to `tools.elevated`.
- **[snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md)** — subagent spawn over ACP; relevance: implements `tools.sessions_spawn`/`subagents` config.
- **[snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md)** — tool registry implementation; relevance: registered-tool-set analog OpenClaw profiles/groups select from.
- **[snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md)** — native MCP tool exposure; relevance: how MCP servers become callable tools the sandbox gate filters.
- **[snippet_example_engine_mcp_tools](../../code_snippets/snippet_example_engine_mcp_tools.md)** — MCP tool surface; relevance: cross-engine view of MCP-as-tools, the `bundle-mcp` concept.

## References

- [OpenClaw Docs — Configuration: tools and custom providers](https://docs.openclaw.ai/gateway/config-tools)
- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Docs — Code mode](https://docs.openclaw.ai/reference/code-mode)
- [OpenClaw Docs — Local models](https://docs.openclaw.ai/gateway/local-models)
- [OpenClaw Docs — Tools and plugins](https://docs.openclaw.ai/tools)

**Source**: OpenClaw documentation — `gateway/config-tools` (mirror `inbox/openclaw_docs/gateway/config-tools.md`), `## Tools` section
**Last Updated**: 2026-06-22
**Status**: Active
