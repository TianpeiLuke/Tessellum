---
tags:
  - resource
  - documentation
  - claude_code
  - web
  - security
keywords:
  - claude code on the web security
  - github authentication options
  - web-setup token sync
  - security and isolation
  - isolated virtual machine
  - credential protection proxy
  - cloud session limitations
  - rate limits
  - ip allowlist
  - cloud session troubleshooting
topics:
  - Claude Code
  - Web & Remote Surfaces
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
access_control_group: ["general"]
---

# Claude Code on the Web — Security, Limits, and Troubleshooting

## Overview

Claude Code on the web runs each task in a fresh Anthropic-managed VM, so its security model is built on **isolation** (per-session VMs separated from your machine and from each other), **network controls**, and **credential protection** (authentication handled through a secure proxy using scoped credentials so secrets never enter the sandbox). Before relying on cloud sessions you must connect GitHub — and understand that GitHub-App installation is *not* a session-level access control — and account for platform limitations (shared rate limits, GitHub-only cloning, organization IP-allowlist incompatibility, no use under Zero Data Retention).

This note collects the cross-cutting security, authentication, limitation, and troubleshooting material for the web surface. The per-session VM contents are covered in [Cloud Environment](cc_cloud_environment.md) and the outbound proxies in [Cloud Network Access](cc_cloud_network_access.md).

## GitHub authentication options

Cloud sessions need access to your GitHub repositories to clone code and push branches. There are two ways to grant access:

- **GitHub App** — authorize the Claude GitHub App during web onboarding. Best for browser onboarding and teams that want Auto-fix.
- **`/web-setup`** — run `/web-setup` in your terminal to sync your local `gh` CLI token to your Claude account. Best for individual developers who already use `gh`.

With either method, a cloud session can access **any repository the connecting GitHub account can see**, not just the repositories the Claude GitHub App is installed on. App installation enables PR webhooks for Auto-fix; **it is not a session-level access control**. To restrict which repositories your team can reach from cloud sessions, restrict access on GitHub itself (for example, by limiting team or repository membership for the connected GitHub accounts).

The GitHub App is required for Auto-fix (which uses the App to receive PR webhooks); if you connect with `/web-setup` and later want Auto-fix, install the App on those repositories. Team and Enterprise admins can disable `/web-setup` with the Quick web setup toggle at claude.ai/admin-settings/claude-code. Organizations with Zero Data Retention enabled cannot use `/web-setup` or other cloud session features.

## Security and isolation

Each cloud session is separated from your machine and from other sessions through several layers:

- **Isolated virtual machines** — each session runs in an isolated, Anthropic-managed VM.
- **Network access controls** — network access is limited by default and can be disabled. When running with network access disabled, Claude Code can still communicate with the Anthropic API, which may allow data to exit the VM.
- **Credential protection** — sensitive credentials such as git credentials or signing keys are never inside the sandbox with Claude Code. Authentication is handled through a secure proxy using scoped credentials.
- **Secure analysis** — code is analyzed and modified within isolated VMs before creating PRs.

## Limitations

Before relying on cloud sessions for a workflow, account for these constraints:

- **Rate limits** — Claude Code on the web shares rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately. There is no separate compute charge for the cloud VM.
- **Repository authentication** — you can only move sessions from web to local when you are authenticated to the same account.
- **Platform restrictions** — repository cloning and pull request creation require GitHub. Self-hosted GitHub Enterprise Server instances are supported for Team and Enterprise plans. GitLab, Bitbucket, and other non-GitHub repositories can be sent to cloud sessions as a local bundle, but the session can't push results back to the remote.
- **Organization IP allowlist** — cloud sessions call the Anthropic API from Anthropic-managed infrastructure, not your network. If your organization has IP allowlisting enabled, every cloud session fails with an authentication error (the same applies to Code Review and Routines). Contact Anthropic support to exempt Anthropic-hosted services from your organization's IP allowlist.

## Troubleshooting cloud sessions

Runtime API errors that appear in the conversation (such as `API Error: 500`, `529 Overloaded`, `429`, or `Prompt is too long`) are shared with the CLI and Desktop app and are covered in the [Error reference](https://code.claude.com/docs/en/errors). The issues below are specific to cloud sessions.

- **Session creation failed** — a new session fails to start or stalls at provisioning, meaning Claude Code could not allocate a cloud environment. Check status.claude.com for incidents, retry after a minute (capacity is provisioned on demand), and confirm the connecting GitHub account has access to the repository (App installation is not required).
- **Remote Control session expired or access denied** — `--teleport` connects through the same Remote Control session infrastructure cloud sessions use, so `Remote Control session expired` or `Access denied` can surface. The connection token is short-lived and scoped to your account: run `/login` locally to refresh credentials, confirm you are signed in to the account that owns the session, and note that `Remote Control may not be available for this organization` means your admin has not enabled cloud sessions for your plan.
- **Environment expired** — cloud sessions stop after inactivity and the environment is reclaimed. Locally this surfaces as `Could not resume session ... its environment has expired. Creating a fresh session instead.`; on the web the session is marked expired. Reopen the session from claude.ai/code to provision a fresh environment with conversation history restored.

The web quickstart adds setup-time issues: **no repositories appear** (verify the connected GitHub account has access; private repos need the same authorization as public ones); **the page only shows a GitHub login button** (cloud sessions require a connected GitHub account); **"Not available for the selected organization"** (an admin must enable the feature); **`/web-setup` returns "Unknown command"** (run it inside the Claude Code CLI, not your shell; if still failing, your CLI is older than v2.1.80 or you are on an API key — run `claude update` then `/login`); **"Could not create a cloud environment"** (run `/web-setup` to create one manually); and **setup script failed** (a non-zero exit blocks startup — add `set -x` to debug, append `|| true` to non-critical commands, and keep the script under the roughly five-minute cache-build budget).

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
