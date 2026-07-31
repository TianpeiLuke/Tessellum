---
tags:
  - resource
  - documentation
  - claude_code
  - plugins
  - marketplace
keywords:
  - strictKnownMarketplaces
  - managed marketplace restrictions
  - plugin source allowlist
  - hostPattern pathPattern
  - exact matching
  - blockedMarketplaces
  - managed settings
  - supply-chain control
topics:
  - Claude Code
  - Plugins
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/plugin-marketplaces
access_control_group: ["general"]
---

# Claude Code — Managed Marketplace Restrictions

## Overview

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the `strictKnownMarketplaces` setting in [managed settings](https://code.claude.com/docs/en/settings). It is an admin/policy control: an allowlist of approved marketplace sources, enforced before any network or filesystem operation, that individual users and project configurations cannot override.

This note covers the allowlist values (undefined / empty / list), the common configuration shapes (exact entries, `hostPattern`, `pathPattern`), when and how the enforcement check runs, the exact-matching rules and their non-normalizing behavior, and how `strictKnownMarketplaces` pairs with `extraKnownMarketplaces`. The full settings reference (all supported source types and the comparison with `extraKnownMarketplaces`) lives in B03A's [`settings.md`](https://code.claude.com/docs/en/settings#strictknownmarketplaces).

## Allowlist values

When `strictKnownMarketplaces` is configured in managed settings, the restriction behavior depends on the value:

| Value               | Behavior                                                         |
| ------------------- | ---------------------------------------------------------------- |
| Undefined (default) | No restrictions. Users can add any marketplace                   |
| Empty array `[]`    | Complete lockdown. Users cannot add any new marketplaces         |
| List of sources     | Users can only add marketplaces that match the allowlist exactly |

## Common configurations

**Disable all marketplace additions** — an empty array locks the org down:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

**Allow specific marketplaces only** — list each approved source. GitHub entries can pin a `ref`, and `url` entries name the full `marketplace.json` URL:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

**Allow all marketplaces from an internal git server** using regex pattern matching on the host. This is the recommended approach for [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server#plugin-marketplaces-on-ghes) or self-hosted GitLab instances:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Allow filesystem-based marketplaces from a specific directory** using regex pattern matching on the path:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Use `".*"` as the `pathPattern` to allow any filesystem path while still controlling network sources with `hostPattern`.

`strictKnownMarketplaces` restricts what users can add, but does not register marketplaces on its own. To make allowed marketplaces available automatically without users running `/plugin marketplace add`, pair it with `extraKnownMarketplaces` in the same `managed-settings.json` (see the [host-and-manage note](cc_host_and_manage_marketplaces.md) for `extraKnownMarketplaces` usage, and B03A's [settings reference](https://code.claude.com/docs/en/settings#strictknownmarketplaces) for using both together).

## How restrictions work

Restrictions are checked **before any network or filesystem operation**. The check runs on marketplace **add** and on plugin **install**, **update**, **refresh**, and **auto-update**. If a marketplace was added before the policy was configured and its source no longer matches the allowlist, Claude Code refuses to install or update plugins from it. The same enforcement applies to `blockedMarketplaces`.

The allowlist uses **exact matching** for most source types. For a marketplace to be allowed, all specified fields must match exactly:

* For GitHub sources: `repo` is required, and `ref` or `path` must also match if specified in the allowlist
* For URL sources: the full URL must match exactly
* For `hostPattern` sources: the marketplace host is matched against the regex pattern
* For `pathPattern` sources: the marketplace's filesystem path is matched against the regex pattern

Exact matching **does not normalize URLs**: a trailing slash, `.git` suffix, or `ssh://` versus `https://` form are treated as different values. If your organization's marketplace can be cloned by more than one URL form, prefer a `hostPattern` entry over a literal URL so all forms match.

Because `strictKnownMarketplaces` is set in [managed settings](https://code.claude.com/docs/en/settings#settings-files), individual users and project configurations **cannot override** these restrictions.

For complete configuration details — including all supported source types and the comparison with `extraKnownMarketplaces` — see B03A's [`strictKnownMarketplaces` reference](https://code.claude.com/docs/en/settings#strictknownmarketplaces).

**Source**: https://code.claude.com/docs/en/plugin-marketplaces
**Last Updated**: 2026-06-13
**Status**: Active
