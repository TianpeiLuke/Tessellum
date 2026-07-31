---
tags:
  - resource
  - documentation
  - claude_code
  - authentication
  - credentials
keywords:
  - claude code authentication
  - browser login
  - paste login code
  - team authentication
  - credential storage
  - apikeyhelper
  - authentication precedence
  - claude_code_oauth_token
  - setup-token
  - long-lived token
topics:
  - Claude Code
  - Authentication
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/authentication
access_control_group: ["general"]
---

# Claude Code — Authentication

## Overview

Claude Code supports multiple authentication methods depending on your setup. Individual users log in with a Claude.ai account, while teams use Claude for Teams or Enterprise, the Claude Console, or a cloud provider (Amazon Bedrock, Google Vertex AI, or Microsoft Foundry). This note is the operational procedure for logging in, setting up team authentication, where credentials are stored per OS, how custom credential scripts and refresh work, the six-tier precedence Claude Code uses when multiple credentials are present, and how to generate a long-lived token for CI.

Cloud-provider setup details (Bedrock/Vertex/Foundry environment variables) live in their own pages — see [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), and [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry).

## Log in to Claude Code

After installing Claude Code, run `claude` in your terminal. On first launch, Claude Code opens a browser window for you to log in.

- If the browser doesn't open automatically, press `c` to copy the login URL to your clipboard, then paste it into your browser.
- If your browser shows a login code instead of redirecting back after you sign in, paste it into the terminal at the `Paste code here if prompted` prompt. This happens when the browser can't reach Claude Code's local callback server, which is common in **WSL2, SSH sessions, and containers**.

You can authenticate with any of these account types:

- **Claude Pro or Max subscription**: log in with your Claude.ai account.
- **Claude for Teams or Enterprise**: log in with the Claude.ai account your team admin invited you to.
- **Claude Console**: log in with your Console credentials. Your admin must have invited you first.
- **Cloud providers**: if your organization uses Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, set the required environment variables before running `claude`. No browser login is needed.

To log out and re-authenticate, type `/logout` at the Claude Code prompt. If you're having trouble logging in, see authentication troubleshooting (`/en/troubleshoot-install#login-and-authentication`).

## Set up team authentication

For teams and organizations, you can configure Claude Code access in one of these ways: Claude for Teams or Enterprise (recommended for most teams), Claude Console, Amazon Bedrock, Google Vertex AI, or Microsoft Foundry.

### Claude for Teams or Enterprise

Claude for Teams and Claude for Enterprise provide the best experience for organizations using Claude Code. Team members get access to both Claude Code and Claude on the web with centralized billing and team management.

- **Claude for Teams**: self-service plan with collaboration features, admin tools, and billing management. Best for smaller teams.
- **Claude for Enterprise**: adds SSO, domain capture, role-based permissions, compliance API, and managed policy settings for organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.

Setup steps: (1) Subscribe to Claude for Teams or contact sales for Claude for Enterprise. (2) Invite team members from the admin dashboard. (3) Team members install Claude Code and log in with their Claude.ai accounts.

### Claude Console authentication

For organizations that prefer API-based billing, you can set up access through the Claude Console:

1. **Create or use a Console account** — use your existing Claude Console account or create a new one.
2. **Add users** — either bulk invite users from within the Console (Settings -> Members -> Invite) or set up SSO.
3. **Assign roles** — when inviting users, assign one of: the **Claude Code** role (users can only create Claude Code API keys) or the **Developer** role (users can create any kind of API key).
4. **Users complete setup** — each invited user accepts the Console invite, checks system requirements, installs Claude Code, and logs in with Console account credentials.

### Cloud provider authentication

For teams using Amazon Bedrock, Google Vertex AI, or Microsoft Foundry: (1) follow the provider setup ([Bedrock](https://code.claude.com/docs/en/amazon-bedrock) / [Vertex](https://code.claude.com/docs/en/google-vertex-ai) / [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) docs). (2) Distribute the environment variables and instructions for generating cloud credentials to your users. (3) Users install Claude Code.

## Credential management

Claude Code securely manages your authentication credentials:

- **Storage location**:
  - On macOS, credentials are stored in the encrypted macOS Keychain.
  - On Linux, credentials are stored in `~/.claude/.credentials.json` with file mode `0600`.
  - On Windows, credentials are stored in `%USERPROFILE%\.claude\.credentials.json` and inherit the access controls of your user profile directory, which restricts the file to your user account by default.
  - If you've set the `CLAUDE_CONFIG_DIR` environment variable on Linux or Windows, the `.credentials.json` file lives under that directory instead.
  - Claude Code manages `.credentials.json` through `/login` and `/logout`. To route requests through a custom API endpoint, set the `ANTHROPIC_BASE_URL` environment variable instead.
- **Supported authentication types**: Claude.ai credentials, Claude API credentials, Azure Auth, Bedrock Auth, and Vertex Auth.
- **Custom credential scripts**: the `apiKeyHelper` setting can be configured to run a shell script that returns an API key.
- **Refresh intervals**: by default, `apiKeyHelper` is called after 5 minutes or on an HTTP 401 response. Set the `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` environment variable for custom refresh intervals.
- **Slow helper notice**: if `apiKeyHelper` takes longer than 10 seconds to return a key, Claude Code displays a warning notice in the prompt bar showing the elapsed time.

`apiKeyHelper`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_AUTH_TOKEN` apply to terminal CLI sessions only. Claude Desktop and cloud sessions use OAuth exclusively and do not call `apiKeyHelper` or read API key environment variables.

### Authentication precedence

When multiple credentials are present, Claude Code chooses one in this order:

1. **Cloud provider credentials**, when `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, or `CLAUDE_CODE_USE_FOUNDRY` is set.
2. **`ANTHROPIC_AUTH_TOKEN`** environment variable. Sent as the `Authorization: Bearer` header. Use this when routing through an LLM gateway or proxy that authenticates with bearer tokens rather than Anthropic API keys.
3. **`ANTHROPIC_API_KEY`** environment variable. Sent as the `X-Api-Key` header. Use this for direct Anthropic API access with a key from the Claude Console. In interactive mode, you are prompted once to approve or decline the key, and your choice is remembered (change it later via the "Use custom API key" toggle in `/config`). In non-interactive mode (`-p`), the key is always used when present.
4. **`apiKeyHelper`** script output. Use this for dynamic or rotating credentials, such as short-lived tokens fetched from a vault.
5. **`CLAUDE_CODE_OAUTH_TOKEN`** environment variable. A long-lived OAuth token generated by `claude setup-token`. Use this for CI pipelines and scripts where browser login isn't available.
6. **Subscription OAuth credentials** from `/login`. This is the default for Claude Pro, Max, Team, and Enterprise users.

If you have an active Claude subscription but also have `ANTHROPIC_API_KEY` set in your environment, the API key takes precedence once approved. This can cause authentication failures if the key belongs to a disabled or expired organization. Run `unset ANTHROPIC_API_KEY` to fall back to your subscription, and check `/status` to confirm which method is active. Claude Code on the Web always uses your subscription credentials; `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` in the sandbox environment do not override them.

### Generate a long-lived token

For CI pipelines, scripts, or other environments where interactive browser login isn't available, generate a one-year OAuth token with `claude setup-token`:

```bash
claude setup-token
```

The command walks you through OAuth authorization and prints a token to the terminal. It does not save the token anywhere; copy it and set it as the `CLAUDE_CODE_OAUTH_TOKEN` environment variable wherever you want to authenticate:

```bash
export CLAUDE_CODE_OAUTH_TOKEN=your-token
```

This token authenticates with your Claude subscription and requires a Pro, Max, Team, or Enterprise plan. It is scoped to inference only and cannot establish Remote Control sessions. Bare mode does not read `CLAUDE_CODE_OAUTH_TOKEN`; if your script passes `--bare`, authenticate with `ANTHROPIC_API_KEY` or an `apiKeyHelper` instead.

> **Note (effective June 15, 2026)**: Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from interactive usage limits.

**Source**: https://code.claude.com/docs/en/authentication
**Last Updated**: 2026-06-13
**Status**: Active
