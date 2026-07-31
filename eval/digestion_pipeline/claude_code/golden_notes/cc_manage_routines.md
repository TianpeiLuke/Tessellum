---
tags:
  - resource
  - documentation
  - claude_code
  - routines
  - management
keywords:
  - manage routines
  - routine detail page
  - run now
  - pause routine
  - branch push permissions
  - claude prefixed branches
  - routine connectors
  - schedule unknown command
  - green status caveat
topics:
  - Claude Code
  - Routines
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/routines
access_control_group: ["general"]
---

# Claude Code — Manage Routines

## Overview

Once a cloud [routine](cc_routines_overview.md) exists, it is managed from its **detail page**, opened by clicking the routine in the list. The detail page shows the routine's repositories, connectors, prompt, schedule, API tokens, GitHub triggers, and a list of past runs. From here you can inspect and open individual runs, run the routine immediately, pause or resume its schedule, edit its configuration, delete it, and control repository branch-push permissions, connectors, and the environment's network access.

This note also covers the two routine **troubleshooting** cases: `/schedule` returning "Unknown command" in the CLI, and routines being disabled by an organization policy.

## View and interact with runs

Click any run to open it as a full session. From there you can see what Claude did, review changes, create a pull request, or continue the conversation. Each run session works like any other session: use the dropdown menu next to the session title to rename, archive, or delete it.

> **Green-status caveat.** A green status in the run list means the session *started and exited without an infrastructure error*. It does **not** mean the task in your prompt succeeded. Open the run to read the transcript and confirm what Claude actually did. Blocked network requests, missing connector tools, and task-level failures all surface in the transcript rather than in the status indicator. Because routines run autonomously, this after-the-fact inspection is how you confirm an outcome.

## Edit and control routines

From the routine detail page you can:

- Click **Run now** to start a run immediately without waiting for the next scheduled time.
- Use the toggle in the **Repeats** section to pause or resume the schedule. Paused routines keep their configuration but don't run until you re-enable them.
- Click the pencil icon to open **Edit routine** and change the name, prompt, repositories, environment, connectors, or any of the routine's triggers. The **Select a trigger** section is where you add or remove schedules, API tokens, and GitHub event triggers (see [Configure triggers](cc_routine_triggers.md)).
- Click the delete icon to remove the routine. Past sessions created by the routine remain in your session list.

## Repositories and branch permissions

Routines need GitHub access to clone repositories. When you create a routine from the CLI with `/schedule`, Claude checks whether your account has GitHub connected and prompts you to run `/web-setup` if it doesn't. See [GitHub authentication options](https://code.claude.com/docs/en/claude-code-on-the-web) for the two ways to grant access.

Each repository you add is cloned on every run. Claude starts from the repository's default branch unless your prompt specifies otherwise.

By default, Claude can only push to branches prefixed with `claude/`. This prevents routines from accidentally modifying protected or long-lived branches. To remove this restriction for a specific repository, enable **Allow unrestricted branch pushes** for that repository when creating or editing the routine.

## Connectors

Routines can use your connected MCP connectors to read from and write to external services during each run. For example, a routine that triages support requests might read from a Slack channel and create issues in Linear.

Connectors are the claude.ai integrations on your account. MCP servers you added locally in the CLI with `claude mcp add` are stored on your machine rather than your claude.ai account, so they do **not** appear in the connectors list. To use one of those servers in a routine, add it as a connector at [claude.ai/customize/connectors](https://claude.ai/customize/connectors), or declare it in a committed `.mcp.json` so it is part of the cloned repository.

When you create a routine, all of your currently connected connectors are included by default. Remove any that aren't needed to limit which tools Claude has access to during the run. You can also add connectors directly from the routine form. To manage or add connectors outside of the routine form, visit **Settings > Connectors** on claude.ai or use `/schedule update` in the CLI. (For the full connector model, see [MCP connectors](https://code.claude.com/docs/en/mcp).)

## Environments and network access

Each routine runs in a [cloud environment](https://code.claude.com/docs/en/claude-code-on-the-web) that controls network access, environment variables, and setup scripts. The routine inherits the environment's network policy on every run.

The **Default** environment uses **Trusted** network access: the default allowlist of package registries, cloud provider APIs, container registries, and common development domains is reachable, but arbitrary domains are not. Outbound requests to other hosts fail with `403` and `x-deny-reason: host_not_allowed`. MCP connector traffic is routed through Anthropic's servers, so the connectors you add to the routine work without adding their hosts to **Allowed domains**.

To allow additional domains, open the routine for editing (pencil icon on the detail page), select the cloud icon showing your environment's name (such as **Default**) below the **Instructions** box, hover over the environment in the list and click the settings icon, then in the **Update cloud environment** dialog change **Network access** to **Custom** and enter your domains in **Allowed domains** (check **Also include default list of common package managers** to keep the default allowlist alongside your custom domains, or select **Full** for unrestricted access). Click **Save changes** — the new policy applies from the next run. See [Network access](https://code.claude.com/docs/en/claude-code-on-the-web) for details on access levels and the default allowlist.

## Troubleshooting

### `/schedule` returns "Unknown command"

The CLI hides `/schedule` when one of its requirements is not met. The cause is usually one of the following:

- You are authenticated with a Console API key or a cloud provider such as Bedrock, Vertex, or Foundry. `/schedule` requires a claude.ai subscription login. If `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` is set in your shell, or `apiKeyHelper` is set in `settings.json`, remove it first, since these take precedence over a claude.ai login.
- `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, or `DISABLE_GROWTHBOOK` is set in your shell environment or in the `env` block of a `settings.json` file. These disable feature-flag fetching, which `/schedule` depends on.
- You are inside a Claude Code on the web session. Manage routines from the web UI instead.
- Your CLI is older than v2.1.81. Run `claude update`.

You can always create and manage routines at [claude.ai/code/routines](https://claude.ai/code/routines) regardless of how the CLI is configured.

### "Routines are disabled by your organization's policy"

Your Team or Enterprise admin has likely turned off the **Routines** toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code). This is a server-side organization setting, so it cannot be overridden from your local configuration. Contact your admin to request that routines be enabled for your organization.

**Source**: https://code.claude.com/docs/en/routines
**Last Updated**: 2026-06-13
**Status**: Active
