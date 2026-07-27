---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - quickstart
keywords:
  - mcp quickstart
  - claude mcp add
  - claude mcp list
  - connection status indicators
  - local stdio server
  - oauth sign-in
  - mcp troubleshooting
  - practical mcp examples
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/mcp-quickstart
access_control_group: ["general"]
---

# Connect an MCP Server: Quickstart

## Overview

This note walks through connecting a single MCP server to Claude Code end to end with the CLI: **add it, check the connection status, use it in a session, then optionally remove it.** The same four steps work for any server — a hosted HTTP server that needs no sign-in, a local `stdio` subprocess, or a hosted server behind OAuth — with only an extra browser sign-in step for the authenticated case. The note also covers the `claude mcp list` status indicators, the worked Sentry / GitHub / PostgreSQL examples, the other surfaces that can add servers, and a symptom-keyed troubleshooting reference.

For the full configuration reference (every transport, scope, auth, and tool-search option) see [`cc_mcp_transports`](cc_mcp_transports.md), [`cc_mcp_installation_scopes`](cc_mcp_installation_scopes.md), [`cc_mcp_authentication`](cc_mcp_authentication.md), and [`cc_mcp_server_management`](cc_mcp_server_management.md).

## Before you begin

Make sure you have Claude Code installed and authenticated, and a terminal open in a project directory (any directory works, including an empty one).

## Add and verify a server

The same flow connects any server: add it, check status, use it, with an optional cleanup at the end. The walkthrough below uses the hosted Claude Code documentation MCP server, which needs no authentication.

**1. Add the MCP server** — run this in your terminal, not inside a `claude` session, because you are configuring the server before starting a conversation:

```bash
claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp
```

The parts: `claude mcp add` registers a server; `--transport http` means the server is hosted at a URL rather than run as a local process; `claude-code-docs` is a name you make up (Claude Code uses it to label the server's tools in output and to refer to it in commands like `claude mcp remove`); the final argument is the hosted URL. The command prints a confirmation noting the server was added "to local config" — `local config` means it is registered to you, in this project only; a server started in a different project would not see it. To register a server once for all projects, add it at user scope (see [`cc_mcp_installation_scopes`](cc_mcp_installation_scopes.md)).

**2. Check the connection status** — confirm the server appears and is healthy:

```bash
claude mcp list
```

The server appears with one of these status indicators:

| Status | Meaning |
| :----- | :------ |
| `✓ Connected` | Ready to use. This is what you should see for `claude-code-docs` |
| `! Needs authentication` | The server is reachable but needs a browser sign-in, or a token passed with `--header` |
| `✗ Failed to connect` | Server didn't respond — see [Troubleshooting](#troubleshooting) |
| `✗ Connection error` | The connection attempt threw an error — see [Troubleshooting](#troubleshooting) |
| `⏸ Pending approval` | A project-scoped server you haven't approved yet |

**3. Use the server** — start a session (`claude`) and ask Claude to use the new server by name, e.g. `Use the claude-code-docs server to look up what MCP_TIMEOUT does`. You don't normally need to name a server (Claude chooses relevant tools on its own), but naming it guarantees the demonstration goes through the new server. The first time Claude calls the server it asks permission to use the new tool; the tool call in the output is labeled with the server name, which is how you confirm the answer came from the MCP server rather than Claude's built-in knowledge.

**4. Remove the server (optional)** — when done experimenting: `claude mcp remove claude-code-docs`. Each connected server takes space in [Claude's context window](https://code.claude.com/docs/en/how-claude-code-works) because its tool names and server instructions load into every session, so removing unused servers keeps that space free.

## Additional server examples

The walkthrough used a hosted no-sign-in server. The other two common shapes use the same add → check → use flow.

**Local `stdio` server (Playwright)** — a `stdio` server is a program Claude Code starts as a subprocess, used for tools needing local resources (a browser, the filesystem, a database socket). The Playwright server gives Claude a browser and runs through `npx` (requires Node.js 18+):

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

This differs from the hosted example in three ways: there is no `--transport` flag (local servers use the default `stdio` transport); everything after the `--` separator is the command Claude Code runs to start the server; and `-y` tells `npx` to install without prompting. The `Added` confirmation means the entry was saved, not that the command ran — the first `claude mcp list` can show `✗ Failed to connect` while `npx` downloads the package, so wait and retry. Then a task like `Use playwright to open https://example.com and tell me the page title` opens a browser window and labels each tool call with the `playwright` server name (e.g. `browser_navigate`). Transport details are in [`cc_mcp_transports`](cc_mcp_transports.md).

**Server requiring sign-in (Sentry)** — hosted services like Sentry, Linear, and Notion run behind OAuth: add the URL, then sign in through the browser. Add the server (`claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`); `claude mcp list` then shows `! Needs authentication`. Start a session, run `/mcp`, select `sentry`, press Enter, and choose `Authenticate` — your browser opens to the sign-in page; approve there and the status changes to connected. Servers that authenticate with a static token instead of OAuth take it at add time with `--header "Authorization: Bearer <token>"`. Auth detail is in [`cc_mcp_authentication`](cc_mcp_authentication.md).

## Practical examples (from the MCP reference)

The MCP reference works the same flow against three real services. After adding each server, debug or query with plain-language prompts:

- **Sentry (monitoring):** `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`, authenticate with `/mcp`, then ask things like "What are the most common errors in the last 24 hours?" or "Which deployment introduced these new errors?".
- **GitHub (code reviews):** authenticates with a fine-grained personal access token passed as a header — `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"` — then prompt "Review PR #456 and suggest improvements" or "Show me all open PRs assigned to me".
- **PostgreSQL (databases):** a local `stdio` server — `claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"` — then query naturally, e.g. "What's our total revenue this month?" or "Show me the schema for the orders table".

## Connect from other surfaces

This walkthrough uses the `claude mcp` CLI, but every Claude Code surface can add MCP servers: the Claude Code desktop app (Connectors UI); the Claude Desktop chat app (a separate app — copy its servers into the CLI with `claude mcp add-from-claude-desktop` on macOS or WSL); [VS Code](https://code.claude.com/docs/en/vs-code); Claude Code on the web (reads `.mcp.json` from your repository); and Claude.ai (connectors added at claude.ai load automatically in the CLI when you sign in with that account). Surface specifics live in the IDE/desktop/web docs.

## Troubleshooting

Check status with `/mcp` inside a session or `claude mcp list` from your shell, then match the symptom:

| Symptom | What to do |
| :------ | :--------- |
| `/mcp` shows **No MCP servers configured** | You likely ran `claude mcp add` from a different project (local servers are tied to where they were added — re-add from this project or use `--scope user`), or edited a config at the wrong path (the only files read are `~/.claude.json` and `<project>/.mcp.json`). |
| **Failed to connect / Connection error** | The server didn't start or the URL didn't respond. For HTTP, `curl -I <url>` (use `curl.exe` in PowerShell): `404`/`405` = up; `401`/`403` = up but needs auth; no response = check URL/network. For stdio, run the configured command directly to see the underlying error; if it starts and waits, you likely omitted the `--` separator. |
| **Connection timed out at startup** | The server exceeded the default 30-second startup timeout (common on a stdio server's first `npx` download). Raise it with `MCP_TIMEOUT` in milliseconds, e.g. `MCP_TIMEOUT=60000 claude`. |
| **Server already exists** | A server with that name already exists at that scope — `claude mcp remove <name>` first, or use a different name. If it exists at more than one scope, pass `--scope` to choose which copy to delete. |
| **Connects but no tools appear** | Run `/mcp` and select the server; an empty tool list usually means a missing required environment variable. Pass it with `--env KEY=value` on `claude mcp add` or in the `env` field of the `.mcp.json` entry. |
| **Changes to `.mcp.json` don't take effect** | Claude Code reads `.mcp.json` at session start — exit and restart. Check `/mcp` for a parse warning on malformed entries. If you previously rejected the server, reset approvals with `claude mcp reset-project-choices`. |
| **OAuth sign-in fails or browser doesn't open** | Run `/mcp`, select the server, choose `Authenticate` again; if the browser doesn't open, copy the URL shown and open it manually. |

## Next steps

With one server connected: browse the Anthropic Directory for more servers (see [`cc_mcp_overview`](cc_mcp_overview.md)); share servers with your team via installation scopes ([`cc_mcp_installation_scopes`](cc_mcp_installation_scopes.md)); manage MCP access org-wide with managed settings ([`cc_managed_mcp_configuration`](cc_managed_mcp_configuration.md)); reference MCP resources with @ mentions and run MCP prompts as commands ([`cc_mcp_tool_search`](cc_mcp_tool_search.md)).

## Related Notes

- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — open AI-tool integration protocol; relevance: this note is the hands-on walkthrough for connecting one MCP server end to end, so the term grounds every step.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic CLI tool; relevance: the entire procedure uses the `claude mcp` CLI subcommands, so the host tool term anchors the walkthrough.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — LLM tool-invocation capability; relevance: the "Use the server" step shows Claude calling the new server's tools, with output labeled by server name — a concrete tool-use event.
- [OAuth 2.0 Token](../../term_dictionary/term_oauth_token.md) — RFC 6749 access/refresh token model; relevance: the "Connect a server that requires sign-in" Sentry example walks through the OAuth browser sign-in, the token-based auth this term defines.
- [VS Code](../../term_dictionary/term_vscode.md) — Microsoft's source-code editor (an IDE surface); relevance: the "Connect from other surfaces" section names VS Code as one place to add MCP servers besides the CLI.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity before granting resource access; relevance: the status table's `! Needs authentication` state and the sign-in flow are authentication steps this term defines, distinct from the token specifics.

**Source**: https://code.claude.com/docs/en/mcp-quickstart
**Last Updated**: 2026-06-13
**Status**: Active
