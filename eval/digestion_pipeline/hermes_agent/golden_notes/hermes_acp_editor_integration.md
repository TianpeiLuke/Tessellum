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

**Source**: `inbox/hermes_agent_docs/user-guide/features/acp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
**Last Updated**: 2026-06-19
**Status**: Active
