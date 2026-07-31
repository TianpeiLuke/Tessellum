---
tags:
  - resource
  - documentation
  - claude_code
  - troubleshooting
  - authentication
keywords:
  - login and authentication
  - reset your login
  - oauth error invalid code
  - 403 forbidden after login
  - anthropic_api_key override
  - oauth login in wsl2 ssh containers
  - token expired
  - bedrock vertex foundry credentials
topics:
  - Claude Code
  - Troubleshooting
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/troubleshoot-install
access_control_group: ["general"]
---

# Claude Code — Login and Authentication Troubleshooting

## Overview

This note covers the **Login and authentication** section of the install-and-login troubleshooting page: login failures, OAuth errors, and token issues that occur when signing in to Claude Code (as distinct from install failures, which are covered in [Install Failures Reference](cc_install_failures_reference.md), and the ordered diagnostic checks plus "Still stuck" escalation in [Install Diagnostics](cc_install_diagnostics.md)). The fixes here are recovery procedures: a clean re-authentication that resolves most cases, recovery from a truncated/expired OAuth code, the 403-after-login subscription/role check, the common `ANTHROPIC_API_KEY` override of a subscription, the headless-browser code-paste flow for WSL2/SSH/containers, token-expiry and macOS Keychain fixes, and re-authenticating the cloud-provider CLI for Bedrock/Vertex/Foundry.

For full cloud-provider setup see [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), and [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry); for the complete credential resolution order see [authentication precedence](https://code.claude.com/docs/en/authentication).

## Reset your login

When login fails and the cause isn't obvious, a clean re-authentication resolves most cases:

1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete the authentication process again

If the browser doesn't open automatically during login, press `c` to copy the OAuth URL to your clipboard, then paste it into a browser manually. This also works when the URL wraps across lines in a narrow or SSH terminal and can't be clicked directly.

## OAuth error: Invalid code

If you see `OAuth error: Invalid code. Please make sure the full code was copied`, the login code expired or was truncated during copy-paste.

**Solutions:**

- Press Enter to retry and complete the login quickly after the browser opens
- Type `c` to copy the full URL if the browser doesn't open automatically
- If using a remote/SSH session, the browser may open on the wrong machine. Copy the URL displayed in the terminal and open it in your local browser instead.

## 403 Forbidden after login

If you see `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` after logging in:

- **Claude Pro/Max users**: verify your subscription is active at [claude.ai/settings](https://claude.ai/settings)
- **Anthropic Console users**: confirm your account has the "Claude Code" or "Developer" role. Admins assign this in the Anthropic Console under Settings → Members.
- **Behind a proxy**: corporate proxies can interfere with API requests. See [network configuration](https://code.claude.com/docs/en/network-config) for proxy setup.

## This organization has been disabled with an active subscription

If you see `API Error: 400 ... "This organization has been disabled"` despite having an active Claude subscription, an `ANTHROPIC_API_KEY` environment variable is overriding your subscription. This commonly happens when an old API key from a previous employer or project is still set in your shell profile.

When `ANTHROPIC_API_KEY` is present and you have approved it, Claude Code uses that key instead of your subscription's OAuth credentials. In non-interactive mode with the `-p` flag, the key is always used when present. See [authentication precedence](https://code.claude.com/docs/en/authentication) for the full resolution order.

To use your subscription instead, unset the environment variable and remove it from your shell profile:

```bash theme={null}
unset ANTHROPIC_API_KEY
claude
```

Check `~/.zshrc`, `~/.bashrc`, or `~/.profile` for `export ANTHROPIC_API_KEY=...` lines and remove them to make the change permanent. On Windows, check your PowerShell profile at `$PROFILE` and your User environment variables for `ANTHROPIC_API_KEY`. Run `/status` inside Claude Code to confirm which authentication method is active.

## OAuth login fails in WSL2, SSH, or containers

When Claude Code runs in WSL2, on a remote machine over SSH, or inside a container, the browser usually opens on a different host and its redirect can't reach Claude Code's local callback server. After you sign in, the browser shows a login code instead of redirecting back automatically. Paste that code into the terminal at the `Paste code here if prompted` prompt to complete login.

If the browser doesn't open at all from WSL2, set the `BROWSER` environment variable to your Windows browser path:

```bash theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

Alternatively, press `c` at the interactive login prompt to copy the OAuth URL, or copy the URL that `claude auth login` prints, and open it in a browser on your local machine.

If pasting the code into the interactive prompt does nothing, your terminal's paste binding likely isn't reaching the input field. Try your terminal's alternate paste shortcut, often right-click or Shift+Insert in Windows Terminal, or use `claude auth login` instead, which reads the pasted code from standard input:

```bash theme={null}
claude auth login
```

This fallback also applies on native Windows or any terminal where pasting into the interactive prompt fails.

## Not logged in or token expired

If Claude Code prompts you to log in again after a session, your OAuth token may have expired.

Run `/login` to re-authenticate. If this happens frequently, check that your system clock is accurate, as token validation depends on correct timestamps.

On macOS, login can also fail when the Keychain is locked or its password is out of sync with your account password, which prevents Claude Code from saving credentials. Run `claude doctor` to check Keychain access. To unlock the Keychain manually, run `security unlock-keychain ~/Library/Keychains/login.keychain-db`. If unlocking doesn't help, open Keychain Access, select the `login` keychain, and choose Edit > Change Password for Keychain "login" to resync it with your account password.

## Bedrock, Vertex, or Foundry credentials not loading

If you configured Claude Code to use a cloud provider and see `Could not load credentials from any providers` on Bedrock, `Could not load the default credentials` on Vertex, or `ChainedTokenCredential authentication failed` on Foundry, your cloud provider CLI is likely not authenticated in the current shell.

For Bedrock, confirm your AWS credentials are valid:

```bash theme={null}
aws sts get-caller-identity
```

For Vertex AI, confirm `ANTHROPIC_VERTEX_PROJECT_ID` and `CLOUD_ML_REGION` are set in your shell, then set application default credentials:

```bash theme={null}
gcloud auth application-default login
```

For Microsoft Foundry, confirm `ANTHROPIC_FOUNDRY_API_KEY` is set, or sign in with the Azure CLI so the default credential chain can find your account:

```bash theme={null}
az login
```

If credentials work in your terminal but not in the VS Code or JetBrains extension, the IDE process likely didn't inherit your shell environment. Set the provider environment variables in the IDE's own settings, or launch the IDE from a terminal where they're already exported. See [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) for full provider setup.

**Source**: https://code.claude.com/docs/en/troubleshoot-install
**Last Updated**: 2026-06-13
**Status**: Active
