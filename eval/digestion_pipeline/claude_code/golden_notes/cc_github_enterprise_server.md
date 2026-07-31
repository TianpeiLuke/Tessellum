---
tags:
  - resource
  - documentation
  - claude_code
  - github_enterprise_server
  - self_hosted
keywords:
  - github enterprise server
  - ghes
  - admin setup
  - github app manifest
  - claude --remote
  - teleport
  - plugin marketplace hostpattern
  - self-hosted git
topics:
  - Claude Code
  - GitHub Enterprise Server
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/github-enterprise-server
access_control_group: ["general"]
---

# Claude Code with GitHub Enterprise Server

## Overview

GitHub Enterprise Server (GHES) support lets an organization use Claude Code against repositories hosted on a self-managed GitHub instance instead of github.com. Once an admin connects the GHES instance, developers can run web sessions, get automated code reviews, and install plugins from internal marketplaces **without any per-repository configuration**. GHES support is available for Team and Enterprise plans.

This note is the operator procedure for that integration: the one-time admin GitHub App setup (guided manifest or manual), network requirements, the developer workflow (auto host-detection, `claude --remote`, `--teleport`), hosting and allowlisting plugin marketplaces on GHES, the feature-support and limitations table, and troubleshooting. For github.com repos, use [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) and [Code Review](cc_code_review.md); to run Claude in your own CI infrastructure, see [GitHub Actions](cc_github_actions.md).

## What works with GitHub Enterprise Server

The table shows which Claude Code features support GHES and any differences from github.com behavior.

| Feature | GHES support | Notes |
| :--- | :--- | :--- |
| Claude Code on the web | Supported | Admin connects the GHES instance once; developers use `claude --remote` or claude.ai/code as usual |
| Code Review | Supported | Same automated PR reviews as github.com |
| Claude Security | Supported | Public beta for Enterprise plans at claude.ai/security |
| Teleport sessions | Supported | Move sessions between web and terminal with `--teleport` |
| Plugin marketplaces | Supported | Use full git URLs instead of `owner/repo` shorthand |
| Contribution metrics | Supported | Delivered via webhooks to the analytics dashboard |
| GitHub Actions | Supported | Requires manual workflow setup; `/install-github-app` is github.com only |
| GitHub MCP server | Not supported | The GitHub MCP server does not work with GHES instances |

## Admin setup

An admin connects the GHES instance to Claude Code **once**; after that, developers use GHES repositories with no additional configuration. You need admin access to your Claude organization and permission to create GitHub Apps on your GHES instance. The guided setup generates a GitHub App manifest and redirects you to your GHES instance to create the app in one click. If your environment blocks the redirect flow, an alternative manual setup is available.

1. **Open Claude Code admin settings** — go to `claude.ai/admin-settings/claude-code` and find the GitHub Enterprise Server section.
2. **Start the guided setup** — click **Connect**. Enter a display name for the connection and your GHES hostname, for example `github.example.com`. If your GHES instance uses a self-signed or private certificate authority, paste the CA certificate in the optional field.
3. **Create the GitHub App** — click **Continue to GitHub Enterprise**. Your browser redirects to your GHES instance with a pre-filled app manifest. Review the configuration and click **Create GitHub App**. GHES redirects you back to Claude with the app credentials stored automatically.
4. **Install the app on your repositories** — from the GitHub App page on your GHES instance, install the app on the repositories or organizations you want Claude to access. You can start with a subset and add more later.
5. **Enable features** — return to `claude.ai/admin-settings/claude-code` and enable Code Review, Claude Security, and contribution metrics for your GHES repositories using the same configuration as github.com.

### GitHub App permissions

The manifest configures the GitHub App with the permissions and webhook events Claude needs across web sessions, Code Review, Claude Security, and contribution metrics:

| Permission | Access | Used for |
| :--- | :--- | :--- |
| Contents | Read and write | Cloning repositories and pushing branches |
| Pull requests | Read and write | Creating PRs and posting review comments |
| Issues | Read and write | Responding to issue mentions |
| Checks | Read and write | Posting Code Review check runs |
| Actions | Read | Reading CI status for auto-fix |
| Repository hooks | Read and write | Receiving webhooks for contribution metrics |
| Metadata | Read | Required by GitHub for all apps |

The app subscribes to `pull_request`, `issue_comment`, `pull_request_review_comment`, `pull_request_review`, and `check_run` events.

### Manual setup

If the guided redirect flow is blocked by your network configuration, click **Add manually** instead of Connect. Create a GitHub App on your GHES instance with the permissions and events above, then enter the app credentials in the form: hostname, OAuth client ID and secret, GitHub App ID, client ID, client secret, webhook secret, and private key.

### Network requirements

Your GHES instance must be reachable from Anthropic infrastructure so Claude can clone repositories and post review comments. If your GHES instance is behind a firewall, allowlist the Anthropic API IP addresses (see [Network configuration](https://code.claude.com/docs/en/network-config)).

## Developer workflow

Once your admin has connected the GHES instance, no developer-side configuration is needed. Claude Code detects your GHES hostname automatically from the git remote in your working directory. Clone a repository from your GHES instance as you normally would, then start a web session — Claude detects the GHES host from your git remote and routes the session through your organization's configured instance:

```bash
git clone git@github.example.com:platform/api-service.git
cd api-service
claude --remote "Add retry logic to the payment webhook handler"
```

The session runs on Anthropic infrastructure, clones your repository from GHES, and pushes changes back to a branch. Monitor progress with `/tasks` or at claude.ai/code. See [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) for the full cloud session workflow including diff review, auto-fix, and routines.

### Teleport sessions to your terminal

Pull a web session into your local terminal with `claude --teleport`. Teleport verifies you are in a checkout of the same GHES repository before fetching the branch and loading the session history. See [teleport requirements](https://code.claude.com/docs/en/claude-code-on-the-web#teleport-requirements) for details.

## Plugin marketplaces on GHES

Host plugin marketplaces on your GHES instance to distribute internal tooling across your organization. The marketplace structure is identical to github.com-hosted marketplaces; the only difference is how you reference them.

### Add a GHES marketplace

The `owner/repo` shorthand always resolves to github.com. For GHES-hosted marketplaces, use the full git URL (HTTPS URLs work as well):

```bash
/plugin marketplace add git@github.example.com:platform/claude-plugins.git
```

See [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) for the full guide to building marketplaces.

### Allowlist GHES marketplaces in managed settings

If your organization uses [managed settings](https://code.claude.com/docs/en/settings) to restrict which marketplaces developers can add, use the `hostPattern` source type to allow all marketplaces from your GHES instance without enumerating each repository:

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

You can also pre-register marketplaces for developers via `extraKnownMarketplaces` (a `git` source with the full GHES URL) so they appear without manual setup. See the `strictKnownMarketplaces` and `extraKnownMarketplaces` settings reference for the complete schema.

## Limitations

A few features behave differently on GHES than on github.com (the feature table summarizes support; these are the workarounds):

- **`/install-github-app` command** — follow the admin setup flow on claude.ai instead. If you also want GitHub Actions workflows on GHES, adapt the example workflow (`anthropics/claude-code-action` `examples/claude.yml`) manually.
- **GitHub MCP server** — use the `gh` CLI configured for your GHES host instead. Run `gh auth login --hostname github.example.com` to authenticate, then Claude can use `gh` commands in sessions.

## Troubleshooting

- **Web session fails to clone repository** — if `claude --remote` fails with a clone error, verify your admin has completed setup for your GHES instance and that the GitHub App is installed on the repository you are working in. Confirm the instance hostname registered in Claude settings matches the hostname in your git remote.
- **Marketplace add fails with a policy error** — if `/plugin marketplace add` is blocked for your GHES URL, your organization has restricted marketplace sources. Ask your admin to add a `hostPattern` entry for your GHES hostname in managed settings.
- **GHES instance not reachable** — if reviews or web sessions time out, your GHES instance may not be reachable from Anthropic infrastructure. Confirm your firewall allows inbound connections from the Anthropic API IP addresses.

**Source**: https://code.claude.com/docs/en/github-enterprise-server
**Last Updated**: 2026-06-13
**Status**: Active
