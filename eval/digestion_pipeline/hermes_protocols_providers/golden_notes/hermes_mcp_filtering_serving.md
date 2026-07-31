---
tags:
  - resource
  - documentation
  - hermes_agent
  - mcp
  - tooling
keywords:
  - mcp tool prefix scheme
  - per-server tool filtering
  - dynamic tool discovery
  - reload-mcp
  - parallel tool calls
  - mcp sampling support
  - hermes mcp serve
  - messaging bridge tools
topics:
  - Hermes Agent
  - MCP
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
access_control_group: ["general"]
---

# Hermes Agent — MCP Filtering, Runtime & Serving

## Overview

This is the runtime half of Hermes's MCP support: how MCP tools are named once registered, how to control which of them Hermes actually sees, and how MCP behaves while the agent runs. It covers the `mcp_<server>_<tool>` prefix scheme, capability-aware utility wrappers, per-server include/exclude filtering (also used as a security control), dynamic tool discovery + `/reload-mcp`, opt-in parallel tool calls, MCP sampling (server-requested inference), and the inverse direction — running `hermes mcp serve` so other MCP-capable agents use Hermes's messaging bridge. The companion note [hermes_mcp_concept_config](hermes_mcp_concept_config.md) covers declaring and configuring MCP servers (catalog, stdio/HTTP/OAuth, mTLS, config keys).

## How Hermes registers MCP tools

Hermes prefixes MCP tools so they do not collide with built-in names:

```text
mcp_<server_name>_<tool_name>
```

Examples of the resulting registered names:

| Server | MCP tool | Registered name |
|---|---|---|
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `create-issue` | `mcp_github_create_issue` |
| `my-api` | `query.data` | `mcp_my_api_query_data` |

In practice you usually do not need to call the prefixed name manually — Hermes sees the tool and chooses it during normal reasoning.

## MCP utility tools

When supported, Hermes also registers utility tools around MCP resources and prompts: `list_resources`, `read_resource`, `list_prompts`, `get_prompt`. These are registered per server with the same prefix pattern, e.g. `mcp_github_list_resources`, `mcp_github_get_prompt`.

These utility tools are **capability-aware**:
- Hermes only registers resource utilities if the MCP session actually supports resource operations.
- Hermes only registers prompt utilities if the MCP session actually supports prompt operations.

So a server that exposes callable tools but no resources/prompts will not get those extra wrappers.

## Per-server filtering

You can control which tools each MCP server contributes, allowing fine-grained management of your tool namespace.

- **Disable a server entirely** — `enabled: false` makes Hermes skip the server completely and not even attempt a connection.
- **Whitelist (`tools.include: [...]`)** — only those server tools are registered.
- **Blacklist (`tools.exclude: [...]`)** — all server tools are registered except the excluded ones.
- **Precedence** — if both `include` and `exclude` are present, `include` wins.
- **Filter utility tools too** — `tools.resources: false` disables `list_resources`/`read_resource`; `tools.prompts: false` disables `list_prompts`/`get_prompt`.

A full example combining whitelist, blacklist, utility-disable, and a disabled server:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [create_issue, list_issues, search_code]
      prompts: false

  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ***"
    tools:
      exclude: [delete_customer]
      resources: false

  legacy:
    url: "https://mcp.legacy.internal"
    enabled: false
```

### What happens if everything is filtered out?

If your config filters out all callable tools and disables or omits all supported utilities, Hermes does not create an empty runtime MCP toolset for that server. That keeps the tool list clean.

## Runtime behavior

- **Discovery time** — Hermes discovers MCP servers at startup and registers their tools into the normal tool registry.
- **Dynamic Tool Discovery** — MCP servers can notify Hermes when their available tools change at runtime by sending a `notifications/tools/list_changed` notification. When Hermes receives it, it automatically re-fetches the server's tool list and updates the registry — no manual `/reload-mcp` required. This is useful for servers whose capabilities change dynamically (e.g. a server that adds tools when a new database schema is loaded, or removes tools when a service goes offline). The refresh is **lock-protected** so rapid-fire notifications from the same server don't cause overlapping refreshes. Prompt and resource change notifications (`prompts/list_changed`, `resources/list_changed`) are received but not yet acted on.
- **Reloading** — if you change MCP config, use `/reload-mcp`, which reloads MCP servers from config and refreshes the available tool list. For runtime tool changes pushed by the server itself, see Dynamic Tool Discovery above.
- **Toolsets** — each configured MCP server also creates a runtime toolset named `mcp-<server>` when it contributes at least one registered tool, making MCP servers easier to reason about at the toolset level.

## Security model

- **Stdio env filtering** — for stdio servers, Hermes does not blindly pass your full shell environment. Only explicitly configured `env` plus a safe baseline are passed through, reducing accidental secret leakage.
- **Config-level exposure control** — the filtering support is also a security control: disable dangerous tools you do not want the model to see, expose only a minimal whitelist for a sensitive server, and disable resource/prompt wrappers when you do not want that surface exposed.

## Example use cases

- **GitHub server with a minimal issue-management surface** — `tools.include: [list_issues, create_issue, update_issue]` plus `prompts: false` / `resources: false` exposes only issue management.
- **Stripe server with dangerous actions removed** — `tools.exclude: [delete_customer, refund_payment]` keeps the read/lookup surface but removes destructive operations.
- **Filesystem server for a single project root** — point the `@modelcontextprotocol/server-filesystem` stdio server at one directory so Hermes can inspect just that project.

## Troubleshooting

- **MCP server not connecting** — verify MCP deps are installed (already in the standard install), check `node --version` / `npx --version`, then verify your config and restart Hermes.
- **Tools not appearing** — possible causes: the server failed to connect; discovery failed; your filter config excluded the tools; the utility capability does not exist on that server; or the server is disabled with `enabled: false`. If you are intentionally filtering, this is expected.
- **Why didn't resource or prompt utilities appear?** — Hermes now only registers those wrappers when both are true: (1) your config allows them, and (2) the server session actually supports the capability. This is intentional and keeps the tool list honest.

## Parallel Tool Calls

By default, MCP tools run sequentially — one at a time. If your MCP server exposes tools that are safe to run concurrently (e.g. read-only queries, independent API calls), you can opt in to parallel execution:

```yaml
mcp_servers:
  docs:
    command: "docs-server"
    supports_parallel_tool_calls: true
```

When `supports_parallel_tool_calls` is `true`, Hermes may execute multiple tools from that server at the same time within a single tool-call batch, just like it does for built-in read-only tools (`web_search`, `read_file`, etc.). Only enable parallel calls for MCP servers whose tools are safe to run at the same time — if tools read and write shared state, files, databases, or external resources, review the read/write race conditions before enabling this setting.

## MCP Sampling Support

MCP servers can request LLM inference from Hermes via the `sampling/createMessage` protocol. This allows a server to ask Hermes to generate text on its behalf — useful for servers that need LLM capabilities but don't have their own model access. Sampling is **enabled by default** for all MCP servers (when the MCP SDK supports it). Configure it per-server under the `sampling` key:

```yaml
mcp_servers:
  my_server:
    command: "my-mcp-server"
    sampling:
      enabled: true            # Enable sampling (default: true)
      model: "openai/gpt-4o"  # Override model for sampling requests (optional)
      max_tokens_cap: 4096     # Max tokens per sampling response (default: 4096)
      timeout: 30              # Timeout in seconds per request (default: 30)
      max_rpm: 10              # Rate limit: max requests per minute (default: 10)
      max_tool_rounds: 5       # Max tool-use rounds in sampling loops (default: 5)
      allowed_models: []       # Allowlist of model names the server may request (empty = any)
      log_level: "info"        # Audit log level: debug, info, or warning (default: info)
```

The sampling handler includes a sliding-window rate limiter, per-request timeouts, and tool-loop depth limits to prevent runaway usage. Metrics (request count, errors, tokens used) are tracked per server instance. To disable sampling for a specific server, set `sampling.enabled: false`.

## Running Hermes as an MCP server

In addition to connecting **to** MCP servers, Hermes can also **be** an MCP server. This lets other MCP-capable agents (Claude Code, Cursor, Codex, or any MCP client) use Hermes's messaging capabilities — list conversations, read message history, and send messages across all your connected platforms.

**When to use this:** you want Claude Code, Cursor, or another coding agent to send and read Telegram/Discord/Slack messages through Hermes; you want a single MCP server that bridges to all of Hermes's connected messaging platforms at once; or you already have a running Hermes gateway with connected platforms.

**Quick start** — `hermes mcp serve` starts a stdio MCP server; the MCP client (not you) manages the process lifecycle. Add Hermes to your MCP client config, for example in Claude Code's `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"]
    }
  }
}
```

### Available tools

The MCP server exposes 10 tools, matching OpenClaw's channel bridge surface plus a Hermes-specific channel browser:

| Tool | Description |
|------|-------------|
| `conversations_list` | List active messaging conversations. Filter by platform or search by name. |
| `conversation_get` | Get detailed info about one conversation by session key. |
| `messages_read` | Read recent message history for a conversation. |
| `attachments_fetch` | Extract non-text attachments (images, media) from a specific message. |
| `events_poll` | Poll for new conversation events since a cursor position. |
| `events_wait` | Long-poll / block until the next event arrives (near-real-time). |
| `messages_send` | Send a message through a platform (e.g. `telegram:123456`, `discord:#general`). |
| `channels_list` | List available messaging targets across all platforms. |
| `permissions_list_open` | List pending approval requests observed during this bridge session. |
| `permissions_respond` | Allow or deny a pending approval request. |

### Event system

The MCP server includes a live event bridge that polls Hermes's session database for new messages, giving clients near-real-time awareness of incoming conversations:

```
# Poll for new events (non-blocking)
events_poll(after_cursor=0)

# Wait for next event (blocks up to timeout)
events_wait(after_cursor=42, timeout_ms=30000)
```

Event types: `message`, `approval_requested`, `approval_resolved`. The event queue is in-memory and starts when the bridge connects; older messages are available through `messages_read`.

### How it works and current limits

The MCP server reads conversation data directly from Hermes's session store (`~/.hermes/sessions/sessions.json` and the SQLite database). A background thread polls the database for new messages and maintains an in-memory event queue. For sending messages, it uses the same `send_message` infrastructure as the Hermes agent itself. The gateway does NOT need to be running for read operations (listing conversations, reading history, polling events); it DOES need to be running for send operations, since the platform adapters need active connections.

Options: `hermes mcp serve` (normal mode) and `hermes mcp serve --verbose` (debug logging on stderr). Current limits: the embedded `hermes mcp serve` exposes a **stdio-only** MCP server today (for HTTP, run a separate adapter — or, much more commonly, use the MCP **client** side, which already speaks both stdio and HTTP); event polling runs at ~200ms intervals via mtime-optimized DB polling (skips work when files are unchanged); no `claude/channel` push notification protocol yet; and `messages_send` is text-only (no media/attachment sending).

## Related Notes

**Terms**
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: this page operates MCP at runtime (prefix/filter/serve).
- [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP aggregation; relevance: `hermes mcp serve` makes Hermes itself the gateway bridging 10 messaging tools.
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool namespace; relevance: the `mcp_<server>_<tool>` prefix scheme + per-server include/exclude shape the registry.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: other MCP clients (incl. agents) consume Hermes' served tools.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — agent-to-agent topology; relevance: `mcp serve` lets Claude Code/Cursor use Hermes' messaging bridge.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: MCP sampling lets servers request inference incl. tool rounds.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session store; relevance: the serve event bridge polls Hermes' session DB.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: dynamic discovery + `/reload-mcp` re-register tools into the running harness.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: Claude Code/Cursor are the served-tool consumers.
- [term_webhook](../../term_dictionary/term_webhook.md) — server push; relevance: `notifications/tools/list_changed` is a server-push akin to a webhook.

**Code-Repos**
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP runtime/filter/serve module; relevance: implements prefix registration, include/exclude filtering, dynamic discovery, `mcp serve`.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + toolsets; relevance: the `mcp-<server>` runtime toolset + utility-tool wrappers live here.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — messaging bridge; relevance: the 10 served tools (`conversations_list`, `messages_send`, …) wrap the gateway's `send_message` + session DB.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes mcp serve` / `/reload-mcp`; relevance: the serve entrypoint + reload slash command.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — sampling inference handler; relevance: MCP sampling (`sampling/createMessage`) routes back through the core conversation loop.

**Snippets**
- [snippet_hermes_agent_tools_mcp_notifications](../../code_snippets/snippet_hermes_agent_tools_mcp_notifications.md) — `notifications/tools/list_changed` handler; relevance: the lock-protected dynamic tool re-discovery this page documents.
- [snippet_hermes_agent_tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — prefixed tool invocation; relevance: calls `mcp_<server>_<tool>` and (when enabled) parallel-batch concurrent tool runs.
- [snippet_hermes_agent_tools_mcp_retry](../../code_snippets/snippet_hermes_agent_tools_mcp_retry.md) — MCP tool retry; relevance: runtime resilience around MCP tool calls.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — registry + prefix scheme; relevance: implements `mcp_<server>_<tool>` namespacing + include/exclude filter application.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: the `mcp-<server>` runtime toolset created per contributing server.
- [snippet_hermes_agent_toolsets_materialize](../../code_snippets/snippet_hermes_agent_toolsets_materialize.md) — toolset materialization; relevance: materializes the per-server toolset (skips empty/fully-filtered servers).
- [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — `hermes mcp serve`; relevance: runs Hermes AS a stdio MCP server with the event bridge.
- [snippet_hermes_agent_mcp_serve_tool_surface](../../code_snippets/snippet_hermes_agent_mcp_serve_tool_surface.md) — the 10 served tools; relevance: `conversations_list`/`messages_send`/`events_poll`/… messaging-bridge surface.
- [snippet_hermes_agent_tools_mcp_lifecycle](../../code_snippets/snippet_hermes_agent_tools_mcp_lifecycle.md) — discovery/reload lifecycle; relevance: `/reload-mcp` + utility-tool capability-aware registration.
- [snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session DB lifecycle; relevance: the serve event bridge polls Hermes' session store for new messages.

**Docs**
- [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — config counterpart; relevance: same protocol, config half.
- [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — served-surface analogue; relevance: serving Hermes' tools over a protocol mirrors serving the agent over HTTP.
- [hermes_acp_editor_integration](hermes_acp_editor_integration.md) — another served protocol; relevance: ACP also exposes a curated tool surface to external clients.
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — `tools.include/exclude` keys; relevance: SP02 owns the filter-config key reference.
- [hermes_subscription_proxy](hermes_subscription_proxy.md) — pass-through serving; relevance: another "serve a Hermes capability to outside clients" surface.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — MCP overview; relevance: analogous MCP runtime model.
- [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — server lifecycle/reload; relevance: analogous to `/reload-mcp` + discovery.
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — tool selection/filtering; relevance: analogous tool-namespace control.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool surface; relevance: served MCP tools sit alongside built-ins.
- [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — SDK MCP wiring; relevance: analogous programmatic MCP registration.

**Source**: `inbox/hermes_agent_docs/user-guide/features/mcp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
**Last Updated**: 2026-06-19
**Status**: Active
