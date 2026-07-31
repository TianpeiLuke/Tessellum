---
tags:
  - resource
  - documentation
  - hermes_agent
  - mcp
  - integration
keywords:
  - use mcp with hermes
  - mcp server config
  - tools include exclude filtering
  - reload-mcp
  - wsl2 chrome-devtools-mcp bridge
  - mcp safe usage allowlist
topics:
  - Hermes Agent
  - Model Context Protocol
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes
access_control_group: ["general"]
---

# Use MCP with Hermes

## Overview

This is the practical, day-to-day **how-to for connecting MCP servers to Hermes Agent** — distinct from the MCP feature page (which explains *what* MCP is). Where the concept page defines the Model Context Protocol, this guide is about getting value from it *quickly and safely*: when to reach for MCP (and when not to), how to install the `.[mcp]` extra, the discipline of adding one safe server first, verifying it loaded with `/reload-mcp`, and — most importantly — filtering each server down to the smallest useful tool surface. It covers the four canonical usage patterns (local-fs, GitHub triage, internal-API, docs/knowledge), an end-to-end tight-whitelist tutorial, the WSL2→Windows-Chrome `chrome-devtools-mcp` stdio bridge, symptom-based troubleshooting, and a recommended first-setups list. The guiding principle throughout: good MCP usage is not "connect everything," it is "connect the right thing, with the smallest useful surface."

## When should you use MCP?

Use MCP when a tool already exists in MCP form and you do not want to build a native Hermes tool; when you want Hermes to operate against a local or remote system through a clean RPC layer; when you want fine-grained per-server exposure control; or when you want to connect Hermes to internal APIs, databases, or company systems without modifying Hermes core.

Do **not** use MCP when a built-in Hermes tool already solves the job well; when the server exposes a huge dangerous tool surface and you are not prepared to filter it; or when you only need one very narrow integration and a native tool would be simpler and safer.

## Mental model

Think of MCP as an **adapter layer**: Hermes remains the agent, MCP servers contribute tools, Hermes discovers those tools at startup or reload time, the model uses them like normal tools, and you control how much of each server is visible. That last part matters — good MCP usage is "connect the right thing, with the smallest useful surface," not "connect everything."

## Step 1: install MCP support

If you installed Hermes with the standard install script, MCP support is already included (the installer runs `uv pip install -e ".[all]"`). To add it separately:

```bash
cd ~/.hermes/hermes-agent
uv pip install -e ".[mcp]"
```

For npm-based servers, make sure Node.js and `npx` are available; for many Python MCP servers, `uvx` is a nice default.

## Step 2: add one server first

Start with a single, safe server — for example, filesystem access to one project directory only. Then start Hermes (`hermes chat`) and ask something concrete ("Inspect this project and summarize the repo layout").

```yaml
mcp_servers:
  project_fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/my-project"]
```

## Step 3: verify MCP loaded

You can verify MCP in a few ways: the Hermes banner/status shows MCP integration when configured; ask Hermes what tools it has available ("Tell me which MCP-backed tools are available right now"); use `/reload-mcp` after config changes; and check logs if the server failed to connect.

## Step 4: start filtering immediately

Do not wait if the server exposes a lot of tools. The canonical pattern is to whitelist only what you want with `tools.include` — usually the best default for sensitive systems:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, search_code]
```

The inverse forms: a remote server can **exclude** dangerous actions (`tools.exclude: [delete_customer, refund_payment]`), and you can **disable utility wrappers** entirely with `tools.resources: false` / `tools.prompts: false`.

## What does filtering actually affect?

There are two categories of MCP-exposed functionality. **(1) Server-native MCP tools** are filtered with `tools.include` / `tools.exclude`. **(2) Hermes-added utility wrappers** are filtered with `tools.resources` / `tools.prompts`. The resource wrappers you may see are `list_resources` / `read_resource`; the prompt wrappers are `list_prompts` / `get_prompt`. These wrappers only appear if your config allows them *and* the MCP server session actually supports those capabilities — Hermes will not pretend a server has resources/prompts if it does not.

## Common patterns

Four canonical setups recur:

- **Pattern 1 — local project assistant**: a repo-local filesystem and/or git server (`@modelcontextprotocol/server-filesystem` rooted at one project dir, `mcp-server-git --repository`) so Hermes reasons over a bounded workspace.
- **Pattern 2 — GitHub triage assistant**: the GitHub server with a tight `include: [list_issues, create_issue, update_issue, search_code]` whitelist and `prompts: false` / `resources: false`, for clustering issues and drafting bug reports.
- **Pattern 3 — internal API assistant**: a remote `url:` server with a `Bearer` header and a strict read-heavy whitelist (`include: [list_customers, get_customer, list_invoices]`) — exactly the place where a whitelist beats an exclude list.
- **Pattern 4 — documentation / knowledge servers**: servers whose value is in prompts/resources (shared knowledge assets) rather than direct actions, so here you deliberately set `prompts: true` / `resources: true`.

## Tutorial: end-to-end setup with filtering

A practical three-phase progression. **Phase 1** adds GitHub MCP with a tight whitelist (the same `include: [list_issues, create_issue, search_code]` + `prompts/resources: false` block), then asks Hermes to summarize the codebase's MCP integration points. **Phase 2** expands the whitelist *only when needed* (add `update_issue`) and reloads with `/reload-mcp`. **Phase 3** adds a second server with a different policy:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue, search_code]
      prompts: false
      resources: false

  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"]
```

Now Hermes can combine them ("Inspect the local project files, then create a GitHub issue summarizing the bug you find") — multi-system workflows without changing Hermes core.

## WSL2: bridge Hermes in WSL to Windows Chrome

The practical setup when Hermes runs inside WSL2, the browser you want to control is your normal signed-in Chrome on Windows, and `/browser connect` is awkward or unreliable. Hermes does **not** connect to Chrome directly — instead Hermes runs in WSL, starts a local stdio MCP server launched through Windows interop (`cmd.exe` / `powershell.exe`), and that server attaches to your live Windows Chrome session. The mental model is `Hermes (WSL) -> MCP stdio bridge -> Windows Chrome`. This keeps your real Windows browser profile, cookies, and logins while Hermes stays in its supported Unix environment, and browser control is exposed as MCP tools instead of Hermes core browser transport.

The recommended server is `chrome-devtools-mcp`. If your Windows Chrome already has live remote debugging enabled (from `chrome://inspect/#remote-debugging`), add it from WSL, then test and reload:

```bash
hermes mcp add chrome-devtools-win --command cmd.exe --args /c npx -y chrome-devtools-mcp@latest --autoConnect --no-usage-statistics
hermes mcp test chrome-devtools-win
```

When Hermes runs in WSL and Chrome runs on Windows, `/browser connect` may fail even though Chrome is open and debuggable — WSL cannot reach the same host-local endpoint Chrome exposes to Windows tools, and newer Chrome debugging flows differ from a classic `ws://localhost:9222`. Keep `/browser connect` for same-environment setups and use MCP for WSL-to-Windows bridging. **Known pitfalls**: start Hermes from a Windows-mounted path like `/mnt/c/Users/<you>` when using Windows stdio executables (starting from `/root` or `/home/...` can emit a `UNC` current-directory warning); if `--autoConnect` times out enumerating pages, reduce background/frozen tabs and retry.

## Safe usage recommendations

The security discipline: **prefer allowlists for dangerous systems** — for anything financial, customer-facing, or destructive, use `tools.include` and start with the smallest set possible. **Disable unused utilities** (`tools.resources: false` / `tools.prompts: false`) if you do not want the model browsing server-provided resources/prompts. **Keep servers scoped narrowly** — a filesystem server rooted to one project dir (not your whole home directory), a git server pointed at one repo, an internal API server with read-heavy exposure by default. And **reload after config changes** with `/reload-mcp` whenever you change include/exclude lists, enabled flags, resources/prompts toggles, or auth headers/env.

## Troubleshooting by symptom

- **"The server connects but the tools I expected are missing"** — filtered by `tools.include`, excluded by `tools.exclude`, utility wrappers disabled, or the server does not actually support resources/prompts.
- **"The server is configured but nothing loads"** — check that `enabled: false` was not left in config, the command/runtime exists (`npx`, `uvx`), the HTTP endpoint is reachable, and auth env/headers are correct.
- **"Why fewer tools than the MCP server advertises?"** — Hermes now respects your per-server policy and capability-aware registration; that is expected and usually desirable.
- **"Remove a server without deleting the config?"** — set `enabled: false`, which keeps the config but prevents connection and registration.

## Recommended first MCP setups

Good first servers for most users: **filesystem**, **git**, **GitHub**, **fetch / documentation** MCP servers, and **one narrow internal API**. Not-great first servers: giant business systems with lots of destructive actions and no filtering, and anything you do not understand well enough to constrain.

## Related Notes

**Terms**
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP servers contribute tools (function-calling) discovered at startup, the concept this how-to puts into practice.
- [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP gateway/proxy layer; relevance: the adapter layer through which contributed tools reach the agent.
- [term_mcp_registry](../../term_dictionary/term_mcp_registry.md) — MCP server registry; relevance: the `mcp_servers.*` config entries this guide adds are registry declarations.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — LLM tool-call mechanism; relevance: discovered MCP tools enter the model as callable functions.
- [term_access_control](../../term_dictionary/term_access_control.md) — least-privilege exposure control; relevance: per-server `include`/`exclude` filtering is the access-control surface this guide centers on.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: remote MCP servers authenticate via OAuth / bearer headers.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the agent runtime; relevance: Hermes remains the harness while MCP servers plug in as tool sources.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: the multi-system MCP workflows this guide enables are the agent's core use case. (+fin: hermes_mcp [own SP09 doc])

**Code-Repos**
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client/lifecycle/toolset surface; relevance: implements add-server, `/reload-mcp`, and the toolset-discovery this how-to drives.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + MCP call/OAuth/retry code; relevance: `tools_mcp_*` (call/oauth/retry/notifications) live here.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `mcp_servers.*` config + `hermes tools` filtering; relevance: the `include`/`exclude`/`resources` filtering CLI and config parsing.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent loop that calls MCP-contributed tools; relevance: discovered MCP tools enter the tool-calling loop here.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — top-level config / `.[mcp]` extras install; relevance: the `pip install .[mcp]` + WSL2 bridge setup is rooted here.

**Snippets**
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — `mcp_servers.*` config parsing; relevance: implements the YAML server declarations this guide writes.
- [snippet_hermes_agent_tools_mcp_client](../../code_snippets/snippet_hermes_agent_tools_mcp_client.md) — MCP client; relevance: the client that connects to each configured server.
- [snippet_hermes_agent_tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — MCP tool call; relevance: how a filtered MCP tool is invoked by the model.
- [snippet_hermes_agent_tools_mcp_lifecycle](../../code_snippets/snippet_hermes_agent_tools_mcp_lifecycle.md) — server lifecycle; relevance: the startup/reload discovery `/reload-mcp` triggers.
- [snippet_hermes_agent_tools_mcp_notifications](../../code_snippets/snippet_hermes_agent_tools_mcp_notifications.md) — MCP notifications; relevance: capability/list-change handling behind tool visibility.
- [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP OAuth flow; relevance: authenticating remote `url:` servers (Pattern 3 internal API).
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — OAuth token manager; relevance: persists/refreshes the bearer credentials remote servers need.
- [snippet_hermes_agent_tools_mcp_retry](../../code_snippets/snippet_hermes_agent_tools_mcp_retry.md) — MCP call retry; relevance: resilience behind the "nothing loads / connect" troubleshooting paths.
- [snippet_hermes_agent_mcp_serve_tool_surface](../../code_snippets/snippet_hermes_agent_mcp_serve_tool_surface.md) — served tool surface; relevance: the filtered tool surface `include`/`exclude` shapes.
- [snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — native MCP skill; relevance: MCP-backed skills the agent loads alongside MCP tools.

**Docs**
- [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: MCP as a non-Python plugin surface alternative to a Python plugin.
- [hermes_plugin_types_surfaces](hermes_plugin_types_surfaces.md) — the surface map; relevance: MCP is one of the config-driven drop-in surfaces enumerated there.
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the scoped-allowlist MCP security tips.
- [hermes_automation_blueprints_event](hermes_automation_blueprints_event.md) — event automation; relevance: MCP tools invoked inside webhook-triggered pipelines.
- [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: MCP-native skills the agent loads.
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — CC MCP model; relevance: closest analogue to the MCP mental model.
- [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — add-an-MCP-server walkthrough; relevance: analogue to Step 1–3.
- [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — managing/reloading MCP servers; relevance: analogue to `/reload-mcp`.
- [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — filtering MCP tools; relevance: analogue to `tools.include`/`exclude`.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — remote MCP OAuth; relevance: analogue to remote-server OAuth auth.
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — CC MCP stdio/SSE/HTTP transports; relevance: analogue to the WSL2→Windows-Chrome stdio bridge transport.
- [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — CC MCP install scopes; relevance: analogue to per-server config placement (`mcp_servers.*`).

**Source**: `inbox/hermes_agent_docs/guides/use-mcp-with-hermes.md` · https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes
**Last Updated**: 2026-06-19
**Status**: Active
