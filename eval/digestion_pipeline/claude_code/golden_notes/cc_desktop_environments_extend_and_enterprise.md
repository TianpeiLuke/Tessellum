---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - enterprise
keywords:
  - desktop environment configuration
  - local cloud ssh sessions
  - sshconfigs sshhostallowlist
  - connectors skills plugins
  - managed settings mdm
  - desktop cli shared configuration
  - cli flag equivalents
  - feature comparison
  - dispatch sessions
topics:
  - Claude Code
  - Desktop application
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/desktop
access_control_group: ["general"]
---

# Claude Desktop — Environments, Extending, and Enterprise

## Overview

The Claude Desktop **Code tab** runs the same engine as the CLI but lets you choose **where** a session executes (Local, Remote/cloud, or SSH), **extend** it with connectors, skills, and plugins through graphical menus, and govern it at scale with **enterprise** admin controls, managed settings, and device-management policies. Because Desktop and the CLI read the same configuration files, your setup carries over. This note covers environment selection, the GUI extension surfaces, the remote/cloud/Dispatch session modes, the org-level governance keys, and the desktop ↔ CLI shared-configuration contract (flag-equivalent and feature-comparison tables plus the "what's not available" list).

Session basics live in [`cc_desktop_overview_and_sessions`](cc_desktop_overview_and_sessions.md), permission modes in [`cc_desktop_permission_modes`](cc_desktop_permission_modes.md), and diff/PR review in [`cc_desktop_diff_review_and_pr`](cc_desktop_diff_review_and_pr.md).

## Remote, continue-in-surface, and Dispatch sessions

### Run long-running tasks remotely

For large refactors, test suites, migrations, or other long-running tasks, select **Remote** instead of **Local** when starting a session. Cloud sessions run on Anthropic's cloud infrastructure and continue even if you close the app or shut down your computer; monitor them from `claude.ai/code` or the Claude iOS app. They support multiple repositories: after selecting a cloud environment, click **+** next to the repo pill to add more repositories, each with its own branch selector — useful for tasks spanning codebases. See [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web).

### Continue in another surface

The **Continue in** menu — from the VS Code icon at the bottom right of the session toolbar — moves your session elsewhere:

* **Claude Code on the Web**: sends your local session to continue remotely. Desktop pushes your branch, generates a conversation summary, and creates a cloud session with the full context; you then archive or keep the local session. Requires a clean working tree; not available for SSH sessions.
* **Your IDE**: opens your project in a supported IDE at the current working directory.

### Sessions from Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) is a persistent conversation with Claude in the **Cowork** tab; you message it a task and it decides how to handle it. A task becomes a Code session two ways: you ask directly ("open a Claude Code session and fix the login bug"), or Dispatch decides it is development work and spawns one (bug fixes, dependency updates, tests, PRs route to Code; research/document/spreadsheet work stays in Cowork). The session appears in the Code-tab sidebar with a **Dispatch** badge and pushes a phone notification when it finishes or needs approval. With computer use enabled, Dispatch sessions can use it too, but app approvals there expire after 30 minutes. Dispatch requires a Pro or Max plan and is not on Team or Enterprise. To compare it with Remote Control, Channels, Slack, and scheduled tasks, see [Platforms and integrations](https://code.claude.com/docs/en/platforms).

## Extend Claude Code

To manage connectors, skills, and plugins in one place, click **Customize** in the sidebar.

### Connect external tools

For local and SSH sessions, click **+** next to the prompt box and select **Connectors** to add integrations like Google Calendar, Slack, GitHub, Linear, and Notion, before or during a session. The **+** button is not available in cloud sessions, but routines configure connectors at routine-creation time. Manage or disconnect from Settings → Connectors or the prompt-box **Manage connectors** menu. **Connectors are [MCP servers](https://code.claude.com/docs/en/mcp) with a graphical setup flow** — for unlisted integrations, add MCP servers manually via settings files, or create custom connectors with remote MCP.

### Use skills

[Skills](https://code.claude.com/docs/en/skills) extend what Claude can do; Claude loads them automatically when relevant, or you invoke one by typing `/` in the prompt box, or clicking **+** → **Slash commands**. This includes built-in commands, your custom skills, project skills from your codebase, and skills from installed plugins. Selecting one highlights it in the input field; type your task after it and send.

### Install plugins

[Plugins](https://code.claude.com/docs/en/plugins) are reusable packages that add skills, agents, hooks, MCP servers, and LSP configurations, installable without the terminal. For local and SSH sessions, click **+** → **Plugins** to see installed plugins; **Add plugin** opens the plugin browser (plugins from your configured marketplaces, including the official Anthropic marketplace), and **Manage plugins** enables, disables, or uninstalls them. Plugins scope to your user account, a project, or local-only; centrally managed plugins behave like in the CLI, and plugins are not available for cloud sessions.

> Preview-server configuration (`.claude/launch.json`), also under "Extend Claude Code" in the source, is owned by [`cc_desktop_diff_review_and_pr`](cc_desktop_diff_review_and_pr.md) since it drives the verify-and-review loop.

## Environment configuration

The environment you pick when starting a session determines where Claude executes and how you connect:

* **Local**: runs on your machine with direct access to your files
* **Remote**: runs on Anthropic's cloud infrastructure; sessions continue even if you close the app
* **SSH**: runs on a remote machine you connect to over SSH, such as your own servers, cloud VMs, or dev containers

### Local sessions

The desktop app does not always inherit your full shell environment. On macOS, launching from the Dock or Finder reads your shell profile (`~/.zshrc` or `~/.bashrc`) to extract `PATH` and a fixed set of Claude Code variables, but other exported variables are not picked up; on Windows, the app inherits user and system environment variables but not PowerShell profiles. To set variables for local sessions and dev servers, open the environment dropdown, hover over **Local**, and click the gear icon to open the **local environment editor**; variables saved there are stored encrypted and apply to every local session and preview server. You can also add variables to the `env` key in `~/.claude/settings.json`, though those reach Claude sessions only.

### Cloud sessions

Cloud sessions continue in the background even if you close the app; usage counts toward your subscription plan limits with no separate compute charges. Create custom cloud environments with different network-access levels and environment variables by selecting the environment dropdown and choosing **Add environment**.

### SSH sessions

SSH sessions run Claude Code on a remote machine while using the desktop app as your interface — useful for codebases on cloud VMs, dev containers, or servers with specific hardware/dependencies. Click the environment dropdown and select **+ Add SSH connection**; the dialog asks for **Name**, **SSH Host** (`user@hostname` or a host in `~/.ssh/config`), **SSH Port** (defaults to 22), and **Identity File** (private-key path; empty uses the default key or SSH config). The remote machine must run Linux or macOS, and Desktop installs Claude Code there automatically on first connect. Once connected, SSH sessions support permission modes, connectors, plugins, and MCP servers.

**Pre-configure SSH connections for a team.** Administrators distribute connections by adding `sshConfigs` to a [managed settings](https://code.claude.com/docs/en/settings#settings-precedence) file; they appear in each user's environment dropdown as managed (selectable but not editable or deletable). Each entry requires `id`, `name`, and `sshHost`; `sshPort`, `sshIdentityFile`, and `startDirectory` are optional. This example opens in `~/projects` on the remote host:

```json
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

Users can also add `sshConfigs` to their own `~/.claude/settings.json` (where dialog-added connections are stored).

**Restrict which SSH hosts users can connect to.** Add `sshHostAllowlist` to a managed settings file to limit Desktop's SSH sessions to approved hosts; an empty array disables SSH sessions entirely. This example allows any host under `devboxes.example.com` plus one named bastion:

```json
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

Patterns are case-insensitive (`*` matches any host, `*.example.com` matches `example.com` and any subdomain, anything else is exact). The check runs against the hostname after `~/.ssh/config` resolution via `ssh -G`, so `Host` aliases and `ProxyCommand`/`ProxyJump` entries pass as long as the resolved `HostName` matches. `sshHostAllowlist` is read from managed settings only (user/project values ignored), only Claude Desktop honors it (not the CLI or IDE extensions, and not `ssh` run through the Bash tool), and it governs which hosts Desktop connects to, not network egress.

## Enterprise configuration

Organizations on Team or Enterprise plans manage desktop behavior through admin console controls, managed settings files, and device-management policies.

### Admin console controls

Configured through the admin settings console: **Code in the desktop** (access to Claude Code in the app), **Code in the web** (web sessions), **Remote Control** ([Remote Control](https://code.claude.com/docs/en/remote-control)), and **Disable Bypass permissions mode**.

### Managed settings

Managed settings override project and user settings and apply when Desktop spawns CLI sessions. Set these keys in your organization's managed settings file or push them remotely through the admin console:

| Key | Description |
| --- | --- |
| `permissions.disableBypassPermissionsMode` | `"disable"` prevents enabling Bypass permissions mode. |
| `disableAutoMode` | `"disable"` prevents enabling Auto mode and removes it from the mode selector. Also accepted under `permissions`. |
| `autoMode` | customize what the auto mode classifier trusts and blocks across your organization. |
| `sshConfigs` | pre-configure SSH connections in the environment dropdown (managed, not user-editable). |
| `sshHostAllowlist` | restrict SSH sessions to hosts matching these patterns; an empty array disables SSH sessions. Read from managed settings only. |
| `managedMcpServers` | push MCP server configs to all users (3P deployments only); each entry specifies a `"http"`/`"sse"`/`"stdio"` transport, connection details, and an optional `toolPolicy` map limiting invocable tools. |

A managed settings file deployed to disk applies to Desktop sessions; settings pushed remotely through the admin console currently reach CLI and IDE sessions only, so for Desktop deployments distribute the file via MDM or use the admin console controls. `permissions.disableBypassPermissionsMode` and `disableAutoMode` also work in user/project settings, but placing them in managed settings prevents overriding. `autoMode` is read from user settings, `.claude/settings.local.json`, and managed settings, but **not** the checked-in `.claude/settings.json` (a cloned repo cannot inject its own classifier rules).

### Device management policies, SSO, data, and deployment

IT teams manage the app through MDM on macOS (`com.anthropic.claudefordesktop` preference domain via Jamf or Kandji) or group policy on Windows (registry at `SOFTWARE\Policies\Claude`); policies enable/disable the Claude Code feature, control auto-updates, and set a custom deployment URL. Organizations can require **SSO** (SAML/OIDC). **Data handling**: code is processed locally in local sessions or on Anthropic's cloud in cloud sessions, with conversations and code context sent to Anthropic's API — see [data handling](https://code.claude.com/docs/en/data-usage). **Deployment**: distribute via MDM (macOS `.dmg`) or MSIX/`.exe` on Windows; for proxy, firewall allowlisting, and LLM gateways see [network configuration](https://code.claude.com/docs/en/network-config).

## Coming from the CLI?

Desktop runs the same underlying engine with a graphical interface; you can run both simultaneously on the same machine and project. Each maintains separate session history, but they **share configuration and project memory via CLAUDE.md files**. To move a CLI session into Desktop, run `/desktop` in the terminal — Claude saves the session, opens it in the desktop app, then exits the CLI (available on macOS and Windows when signed in with a Claude subscription; not available with API-key auth or on Bedrock, Vertex, or Foundry).

### CLI flag equivalents

| CLI | Desktop equivalent |
| --- | --- |
| `--model sonnet` | Model dropdown next to the send button |
| `--resume`, `--continue` | Click a session in the sidebar |
| `--permission-mode` | Mode selector next to the send button |
| `--dangerously-skip-permissions` | Bypass permissions mode (Settings → "Allow bypass permissions mode"; admins can disable) |
| `--add-dir` | Add repos with the **+** button in cloud sessions |
| `--allowedTools`, `--disallowedTools` | No per-session equivalent; settings-file rules still apply |
| `--verbose` | Verbose view mode in the Transcript view dropdown |
| `--print`, `--output-format` | Not available; Desktop is interactive only |
| `ANTHROPIC_MODEL` env var | Model dropdown next to the send button |
| `MAX_THINKING_TOKENS` env var | Set in the local environment editor |

### Shared configuration

Desktop and CLI read the same files: **CLAUDE.md** / `CLAUDE.local.md`, **MCP servers** in `~/.claude.json` or `.mcp.json`, **hooks** and **skills** in settings, **settings** in `~/.claude.json` and `~/.claude/settings.json` (permission rules, allowed tools), and the same **models**. Desktop additionally loads MCP servers from `claude_desktop_config.json` into Code-tab sessions; the standalone CLI does not read that file, so on macOS and WSL run `claude mcp add-from-claude-desktop` to copy them into `~/.claude.json`.

### Feature comparison and what's not available

The CLI-vs-Desktop matrix marks the boundary: permission modes are all-modes-including-`dontAsk` (CLI) versus the five GUI modes; MCP is settings-file versus the Connectors UI for local/SSH; plugins are `/plugin` versus the plugin-manager UI; session isolation is the [`--worktree`](https://code.claude.com/docs/en/cli-reference) flag versus automatic worktrees; multiple sessions are separate terminals versus sidebar tabs; recurring work is cron/CI versus [scheduled tasks](cc_desktop_scheduled_tasks.md); and scripting/automation (`--print`, the Agent SDK) is CLI-only. **What's not available in Desktop**: third-party providers (default Anthropic API, with the Cowork on 3P research preview as the exception), Linux (macOS/Windows only), inline code suggestions, agent teams (CLI-only — use [dynamic workflows](https://code.claude.com/docs/en/workflows) inside one session), and terminal-dialog commands such as `/permissions`, `/config`, `/agents`, and `/doctor` (which reply `isn't available in this environment`).

## Troubleshooting (desktop-specific)

The desktop app has its own troubleshooting set: check your version (macOS **Claude → About Claude**; Windows **Help → About**); fix **403 / authentication errors** by signing out and back in, verifying a paid subscription, fully quitting and reopening, and checking network/proxy; recover a **blank or stuck launch** by restarting, checking for updates, and (Windows) reading Event Viewer crash logs; resolve **"Failed to load session"** by trying a different folder; fix **sessions not finding tools** by verifying `PATH` in the shell profile and restarting; install **Git / Git LFS** when required; and address **MCP servers not working on Windows** by checking config, restarting, and reviewing logs. Cloud sessions can create branches not present locally — when the CLI shows **"Branch doesn't exist yet,"** copy the branch name from the session toolbar and fetch it:

```bash
git fetch origin <branch-name>
git checkout <branch-name>
```

Runtime API errors that appear in the chat (`API Error: 500`, `529 Overloaded`, `429`, `Prompt is too long`) are the same across CLI, desktop, and web — see the [Error reference](https://code.claude.com/docs/en/errors).

**Source**: https://code.claude.com/docs/en/desktop
**Last Updated**: 2026-06-13
**Status**: Active
