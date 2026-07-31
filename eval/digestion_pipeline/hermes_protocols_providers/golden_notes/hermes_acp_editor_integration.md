---
tags:
  - resource
  - documentation
  - hermes_agent
  - acp
  - editor_integration
keywords:
  - acp editor integration
  - agent client protocol
  - hermes acp server
  - vs code zed jetbrains
  - hermes-acp toolset
  - session-scoped auto-approval
topics:
  - Hermes Agent
  - ACP Editor Integration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
access_control_group: ["general"]
---

# Hermes Agent — ACP Editor Integration

## Overview

ACP editor integration is the procedure for running Hermes Agent **as an ACP (Agent Client Protocol) server** so ACP-compatible editors — VS Code, Zed, JetBrains — talk to Hermes over stdio and render chat, tool activity, file diffs, terminal commands, approval prompts, and streamed thinking/response chunks. It is the right fit when you want Hermes to behave like an editor-native coding agent instead of a standalone CLI or messaging bot. In this mode Hermes runs a curated `hermes-acp` toolset, reuses the same `~/.hermes/` config/credentials/state as the CLI, binds each session to the editor's working directory, and exposes a 4-tier approval model (allow once / allow for session / allow always / deny). The ACP *protocol concept* is owned by the term note [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md); this note documents how to USE it inside Hermes.

## What Hermes exposes in ACP mode

Hermes runs with a curated `hermes-acp` toolset designed for editor workflows. It includes:

- file tools: `read_file`, `write_file`, `patch`, `search_files`
- terminal tools: `terminal`, `process`
- web/browser tools
- memory, todo, session search
- skills
- execute_code and delegate_task
- vision

It intentionally excludes things that do not fit typical editor UX, such as messaging delivery and cronjob management.

## Installation

Install Hermes normally, then add the ACP extra:

```bash
pip install -e '.[acp]'
```

This installs the `agent-client-protocol` dependency and enables `hermes acp`, `hermes-acp`, and `python -m acp_adapter`.

For Zed registry installs, Zed launches Hermes through the official ACP Registry entry, which uses a `uvx` distribution that runs `uvx --from 'hermes-agent[acp]==<version>' hermes-acp`. Make sure `uv` is available on `PATH` before using the registry install path.

### Browser tools (optional)

Browser tools (`browser_navigate`, `browser_click`, etc.) depend on the `agent-browser` npm package and Chromium, which aren't part of the Python wheel. Install them with:

```bash
hermes acp --setup-browser           # interactive (prompts before ~400 MB download)
hermes acp --setup-browser --yes     # accept the download non-interactively
```

This is the standalone command. The Zed registry's terminal-auth flow (`hermes acp --setup`) also offers the browser bootstrap as a follow-up question after model selection, so most users never need to run `--setup-browser` directly. The bootstrap installs Node.js 22 LTS into `~/.hermes/node/` if missing, runs `npm install -g agent-browser @askjo/camofox-browser` into that user-writable prefix (no sudo), and installs Playwright Chromium (or reuses a detected system Chrome/Chromium). It is idempotent — re-running skips work already done.

## Launching the ACP server

Any of the following starts Hermes in ACP mode:

```bash
hermes acp
hermes-acp
python -m acp_adapter
```

Hermes logs to stderr so stdout remains reserved for ACP JSON-RPC traffic. For non-interactive checks: `hermes acp --version` and `hermes acp --check`.

## Editor setup

### VS Code

Install the **ACP Client** extension. To connect: open the ACP Client panel from the Activity Bar, select **Hermes Agent** from the built-in agent list, then connect and start chatting. To define Hermes manually, add it through VS Code settings under `acp.agents`:

```json
{
  "acp.agents": {
    "Hermes Agent": {
      "command": "hermes",
      "args": ["acp"]
    }
  }
}
```

### Zed

Zed v0.221.x and newer installs external agents through the official ACP Registry: open the Agent Panel, click **Add Agent** (or run the `zed: acp registry` command), search for **Hermes Agent**, install it, and start a new Hermes external-agent thread. Prerequisites: configure Hermes provider credentials first (`hermes model`, or `~/.hermes/.env` / `~/.hermes/config.yaml`), and install `uv` so the registry launcher can run `uvx --from 'hermes-agent[acp]==<version>' hermes-acp`. For local development before the registry entry is available, use a custom agent server in Zed settings:

```json
{
  "agent_servers": {
    "hermes-agent": {
      "type": "custom",
      "command": "hermes",
      "args": ["acp"]
    }
  }
}
```

### JetBrains

Use an ACP-compatible plugin and point it at `/path/to/hermes-agent/acp_registry`.

## Registry manifest

The source copy of Hermes' official ACP Registry metadata lives at `acp_registry/agent.json` and `acp_registry/icon.svg`. The upstream registry PR copies those files into the top-level `hermes-agent/` directory in `agentclientprotocol/registry`. The registry entry uses a `uvx` distribution that points directly at the `hermes-agent` PyPI release (`uvx --from 'hermes-agent[acp]==<version>' hermes-acp`). The registry CI verifies that the pinned version exists on PyPI, so the manifest's `version` and uvx `package` pin must always match `pyproject.toml`; `scripts/release.py` keeps them in lockstep automatically.

## Configuration and credentials

ACP mode uses the same Hermes configuration as the CLI: `~/.hermes/.env`, `~/.hermes/config.yaml`, `~/.hermes/skills/`, and `~/.hermes/state.db`. Provider resolution uses Hermes' normal runtime resolver, so ACP inherits the currently configured provider and credentials. Hermes also advertises a terminal auth method (`--setup`) for first-run registry clients; this opens Hermes' interactive model/provider setup.

## Session behavior

ACP sessions are tracked by the ACP adapter's in-memory session manager while the server is running. Each session stores its session ID, working directory, selected model, current conversation history, and cancel event. The underlying `AIAgent` still uses Hermes' normal persistence/logging paths, but ACP `list/load/resume/fork` are scoped to the currently running ACP server process.

## Working directory behavior

ACP sessions bind the editor's cwd to the Hermes task ID so file and terminal tools run relative to the editor workspace, not the server process cwd.

## Approvals

Dangerous terminal commands can be routed back to the editor as approval prompts. ACP approval options are simpler than the CLI flow — allow once, allow always, deny — and on timeout or error the approval bridge denies the request.

### Session-scoped edit auto-approval

ACP exposes a third tier between *allow once* and *allow always*: **Allow for session**. Picking it from the editor's permission prompt records the approval inside the current ACP session only — every subsequent matching command in that session goes through without prompting, but a new ACP session (or restarting the editor) resets the slate and re-prompts the first time.

| Option | Editor label | Scope | Persisted across restarts |
|---|---|---|---|
| `allow_once` | Allow once | This one tool call | No |
| `allow_session` | Allow for session | All matching calls in this ACP session | No — cleared when the session ends |
| `allow_always` | Allow always | All future sessions | Yes (written to the Hermes permanent allowlist) |
| `deny` | Deny | This one tool call | No |

`allow_session` is the right default for an editor workflow where you trust an agent for the duration of a task but don't want to grant a long-lived allowlist entry. The safety trade-off is straightforward: the broader the scope, the less the editor will interrupt you, and the more damage a misbehaving agent (or prompt injection) can do before you notice. Start with `allow_once` for unfamiliar commands; promote to `allow_session` once you've seen the agent run the same pattern correctly a few times; reserve `allow_always` for truly idempotent commands you trust forever (e.g. `git status`). The ACP bridge maps these options onto Hermes' internal approval semantics — `allow_always` writes a permanent allowlist entry the same way the CLI does, while `allow_session` only affects the in-process approval cache for the current ACP session.

## Troubleshooting

- **ACP agent does not appear in the editor** — In Zed, open the ACP Registry with `zed: acp registry` and search for **Hermes Agent**. For manual/local development, verify the custom `agent_servers` command points to `hermes acp`. Confirm Hermes is installed and on your PATH, the ACP extra is installed (`pip install -e '.[acp]'`), and `uv` is installed if launching from the official Zed registry entry.
- **ACP starts but immediately errors** — Run `hermes acp --version`, `hermes acp --check`, `hermes doctor`, and `hermes status`.
- **Missing credentials** — ACP mode uses Hermes' existing provider setup. Configure credentials with `hermes model` or by editing `~/.hermes/.env`. Registry clients can also trigger Hermes' terminal auth flow, which runs the same interactive provider/model setup.
- **Zed registry launcher cannot find uv** — Install `uv` from the official uv installation docs, then retry the Hermes Agent thread from Zed.

The ACP internals, provider-runtime resolution, and tools-runtime developer references are documented in the developer-guide sub-plan (SP18); the optional browser-tools setup detail is owned by the browser sub-plan (SP08).

## Related Notes

**Terms**
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON-RPC over stdio; relevance: ACP speaks JSON-RPC; Hermes logs to stderr to keep stdout clean.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: the curated `hermes-acp` toolset includes `delegate_task`.
- [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — human approval gate; relevance: dangerous terminal commands route back as editor approval prompts.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: ACP `list/load/resume/fork` reuse Hermes' normal persistence paths.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — execution sandbox; relevance: file/terminal/execute_code tools run relative to the editor cwd.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the underlying `AIAgent` powers each ACP session.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: ACP renders tool activity (file diffs, terminal) as the agent's tool calls.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — editor-native coding agent; relevance: ACP makes Hermes behave like an editor-native coding agent.
- [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the ACP concept term (active); relevance: this note is the Hermes-editor ACP integration procedure that LINKs the existing concept term.
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool namespace; relevance: the curated toolset is a filtered registry view.
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the sibling stdio editor/agent protocol.

**Code-Repos**
- [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — the ACP adapter module; relevance: implements `hermes acp`/`hermes-acp`/`acp_adapter`, in-memory session manager, approval bridge, registry manifest.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `hermes-acp` toolset; relevance: the curated file/terminal/web/memory/skills toolset exposed in ACP mode.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes acp --setup/--check/--setup-browser`; relevance: the launch + browser-bootstrap commands.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` + approval semantics; relevance: ACP options map onto Hermes' internal allow-once/session/always approval cache.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider resolution; relevance: ACP inherits the normal runtime provider/credential resolver.

**Snippets**
- [snippet_hermes_agent_acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — `hermes acp` entrypoint; relevance: the launch command + stderr-only logging this page documents.
- [snippet_hermes_agent_acp_server_init](../../code_snippets/snippet_hermes_agent_acp_server_init.md) — ACP server init; relevance: boots the JSON-RPC-over-stdio ACP server.
- [snippet_hermes_agent_acp_server_session_methods](../../code_snippets/snippet_hermes_agent_acp_server_session_methods.md) — session list/load/resume/fork; relevance: the ACP session methods reusing Hermes persistence.
- [snippet_hermes_agent_acp_server_prompt](../../code_snippets/snippet_hermes_agent_acp_server_prompt.md) — prompt/turn handling; relevance: drives each `AIAgent` turn inside an ACP session.
- [snippet_hermes_agent_acp_session](../../code_snippets/snippet_hermes_agent_acp_session.md) — in-memory session manager; relevance: the editor-cwd-bound in-memory ACP session state.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — `hermes-acp` toolset; relevance: registers the curated file/terminal/web/memory/skills toolset.
- [snippet_hermes_agent_acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — approval bridge; relevance: maps the 4-tier allow-once/session/always/deny model to editor prompts.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest; relevance: the editor registry-manifest (VS Code/Zed/JetBrains) this page configures.
- [snippet_hermes_agent_acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — ACP credential resolution; relevance: ACP inherits the normal provider/credential resolver (§Configuration and credentials).
- [snippet_hermes_agent_acp_server_module_helpers](../../code_snippets/snippet_hermes_agent_acp_server_module_helpers.md) — ACP server helpers; relevance: working-directory binding + browser-tools bootstrap helpers (`--setup-browser`).

**Docs**
- [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md) — served-tool sibling; relevance: ACP and MCP-serve both expose curated tool surfaces.
- [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — MCP config; relevance: ACP and MCP are the two external-protocol surfaces.
- [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — HTTP agent surface; relevance: third way to drive the agent from outside.
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — `~/.hermes/config.yaml`; relevance: ACP reuses the same config/env/skills/state.db.
- [hermes_fallback_providers](hermes_fallback_providers.md) — provider resilience; relevance: ACP inherits the configured fallback chain.
- [cc_vs_code_extension](../claude_code/cc_vs_code_extension.md) — VS Code agent integration; relevance: direct analogue to the VS Code ACP setup.
- [cc_jetbrains_plugin](../claude_code/cc_jetbrains_plugin.md) — JetBrains plugin; relevance: direct analogue to the JetBrains ACP path.
- [cc_vs_code_ide_mcp_server](../claude_code/cc_vs_code_ide_mcp_server.md) — IDE-as-server; relevance: editor↔agent over a local protocol, like ACP-over-stdio.
- [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — approval handling; relevance: analogous to the 4-tier ACP approval model.
- [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — permission modes; relevance: allow-once/session/always parallels CC permission scopes.

**Source**: `inbox/hermes_agent_docs/user-guide/features/acp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
**Last Updated**: 2026-06-19
**Status**: Active
