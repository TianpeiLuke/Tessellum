---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - org_enforcement
keywords:
  - sandbox org enforcement
  - managed settings sandbox
  - failifunavailable
  - allowunsandboxedcommands false
  - allowmanagedreadpathsonly
  - allowmanageddomainsonly
  - keep developers from widening policy
  - custom mitm proxy
  - server-managed settings
  - excludedcommands lockdown
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/sandboxing
access_control_group: ["general"]
---

# Claude Code — Enforce the Sandbox Across an Organization

## Overview

An organization can **require** the built-in Bash sandbox for every developer, **stop developers from widening** the policy, and **route sandbox traffic through a corporate proxy** by delivering the `sandbox` settings keys through **managed settings**. The built-in Bash sandbox is the only isolation approach Claude Code enforces itself — dev containers, custom containers, and VMs are conventions or device-management concerns, not boundaries Claude Code requires. This note is the admin procedure: which keys to deploy, how boolean-override vs array-merge semantics determine what developers can change, the `allowManagedReadPathsOnly`/`allowManagedDomainsOnly` lockdowns, and the custom MITM proxy configuration.

## Which approaches an organization can enforce

Individual developers can opt into any isolation approach, but what an organization can *enforce* — and with which tools — depends on the approach:

- **Built-in Bash sandbox** — the only approach Claude Code enforces itself. Deliver the `sandbox` settings keys through managed settings, either as a file managed by your MDM or through [server-managed settings](https://code.claude.com/docs/en/server-managed-settings) on Claude.ai.
- **Dev containers** — committing the example dev container to your repositories standardizes the environment across a team, but this is a *convention* rather than an enforcement boundary, because Claude Code does not require a container. If developers should not be able to run Claude Code outside it, enforce that with your organization's device management or software allowlisting tools.
- **Custom containers and VMs** — distribute Claude Code through the approved image and use your organization's device management or software allowlisting tools to prevent installation outside it.

## Enforce sandboxing with managed settings

To require the sandbox for every developer, deliver the `sandbox` keys through [managed settings](https://code.claude.com/docs/en/settings#settings-files), either as a file managed by your MDM or through [server-managed settings](https://code.claude.com/docs/en/server-managed-settings) on Claude.ai.

The following managed settings configuration enables the sandbox, refuses to start Claude Code if the sandbox cannot initialize, and prevents the model from retrying commands outside the sandbox:

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

The two keys beyond `enabled` control what happens when the sandbox cannot run a command:

- **`failIfUnavailable`** — a missing dependency such as bubblewrap on Linux blocks Claude Code from starting rather than showing a warning and falling back to unsandboxed execution.
- **`allowUnsandboxedCommands: false`** — the `dangerouslyDisableSandbox` escape hatch is ignored, so commands that fail under the sandbox cannot be retried outside it.

Two additions are worth considering alongside them:

- Add `excludedCommands` for any organization-approved tools that must run without isolation.
- Add `denyRead` entries for credential directories such as `~/.aws` and `~/.ssh`, which the default read policy still allows.

The sandbox does not run on native Windows, so if your fleet includes Windows hosts, scope this configuration to macOS and Linux or have those users run Claude Code inside WSL2 or a container.

## Keep developers from widening the policy

How a managed value interacts with a developer's local setting depends on whether the key is a boolean or an array:

- **Boolean keys** such as `enabled` and `failIfUnavailable` — Claude Code uses the managed value and ignores anything a developer sets locally.
- **Array keys** such as `excludedCommands` and `allowRead` — Claude Code merges entries from every scope, so a developer can append entries that *widen* the policy.

To stop developers from widening read access, set `allowManagedReadPathsOnly` to `true` in managed settings. Then only `allowRead` entries from managed settings are honored; user, project, and local `allowRead` entries are ignored. This prevents developers from widening read access beyond the organization-approved paths. To lock network domains to the managed values the same way, set `allowManagedDomainsOnly`.

`excludedCommands` has **no** equivalent managed-only lockdown, so a developer can always append entries that run additional commands outside the sandbox. Keep the managed list narrow.

## Custom proxy configuration

For organizations requiring advanced network security, you can implement a custom proxy to:

- Decrypt and inspect HTTPS traffic
- Apply custom filtering rules
- Log all network requests
- Integrate with existing security infrastructure

To point Claude Code at your proxy, set the proxy ports in sandbox settings:

```json
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

A custom proxy that terminates TLS and inspects traffic (with its CA certificate installed inside the sandbox) is the recommended path when the built-in hostname-only proxy is insufficient for your threat model.

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
