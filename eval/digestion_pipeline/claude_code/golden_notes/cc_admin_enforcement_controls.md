---
tags:
  - resource
  - documentation
  - claude_code
  - admin
  - enforcement
keywords:
  - managed settings enforcement
  - permission rules and lockdown
  - sandboxing network allowlist
  - mcp and plugin lockdown
  - usage visibility
  - data handling
  - version floor
  - disable agent view
topics:
  - Claude Code
  - Admin
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/admin-setup
access_control_group: ["general"]
---

# Claude Code — Admin Enforcement Controls

## Overview

Once an administrator has chosen a provider and a settings-delivery mechanism, the next deployment step is deciding **what to enforce, what to watch, and how data is handled**. Managed settings can lock down tools, sandbox execution, restrict MCP servers and plugin sources, control which hooks run, and pin a version floor — each control surface being a row in the enforcement catalog with the specific setting keys that drive it. Because managed values take precedence over user and project settings (and array keys merge rather than replace), developers can extend managed lists but not remove from them. This note catalogs the enforcement controls, the permission-vs-sandbox layering distinction, and the usage-visibility and data-handling matrices an admin reviews. Each control links to its home reference page; this note is the operational catalog, not the per-feature deep dive.

## Decide what to enforce

Managed settings can lock down tools, sandbox execution, restrict MCP servers and plugin sources, and control which hooks run. Each control below is a surface with the setting keys that drive it.

| Control | What it does | Key settings |
| :--- | :--- | :--- |
| Permission rules | Allow, ask, or deny specific tools and commands | `permissions.allow`, `permissions.deny` |
| Permission lockdown | Only managed permission rules apply; disable `--dangerously-skip-permissions` | `allowManagedPermissionRulesOnly`, `permissions.disableBypassPermissionsMode` |
| Sandboxing | OS-level filesystem and network isolation with domain allowlists | `sandbox.enabled`, `sandbox.network.allowedDomains` |
| Managed policy CLAUDE.md | Org-wide instructions loaded in every session, cannot be excluded | File at the managed policy path |
| MCP server control | Restrict which MCP servers users can add or connect to, or deploy a fixed set | `allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`, or a deployed `managed-mcp.json` file |
| Plugin marketplace control | Restrict which marketplace sources users can add and install from | `strictKnownMarketplaces`, `blockedMarketplaces` |
| Customization lockdown | Block skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings | `strictPluginOnlyCustomization` |
| Hook restrictions | Only managed hooks load; restrict HTTP hook URLs | `allowManagedHooksOnly`, `allowedHttpHookUrls` |
| Disable agent view | Turn off `claude agents`, `--bg`, `/background`, and the on-demand supervisor | `disableAgentView` |
| Version floor | Prevent auto-update from installing below an org-wide minimum | `minimumVersion` |
| Required version range | Refuse to start at all when the running version is outside an org-approved range. Stronger than `minimumVersion`, which only blocks downgrades | `requiredMinimumVersion`, `requiredMaximumVersion` |

Detail for each control surface lives on its own reference page: Permissions (rules + managed-only lockdown), [Sandboxing](https://code.claude.com/docs/en/sandboxing), organization-wide CLAUDE.md, managed MCP, plugin-marketplace restrictions, hook configuration, and agent view.

### Permission rules and sandboxing cover different layers

Permission rules and sandboxing are complementary layers, not substitutes. Denying `WebFetch` blocks Claude's fetch tool, **but if `Bash` is allowed, `curl` and `wget` can still reach any URL**. Sandboxing closes that gap with a network domain allowlist enforced at the OS level. So a complete egress posture requires both: deny the high-level tool *and* constrain shell network access through the sandbox allowlist. For the threat model these controls defend against, see [Security](https://code.claude.com/docs/en/security).

## Set up usage visibility

Choose monitoring based on what you need to report on.

| Capability | What you get | Availability | Where to start |
| :--- | :--- | :--- | :--- |
| Usage monitoring | OpenTelemetry export of sessions, tools, and tokens | All providers | Monitoring usage |
| Analytics dashboard | Per-user metrics, contribution tracking, leaderboard | Anthropic only | Analytics |
| Cost tracking | Spend limits, rate limits, and usage attribution | Anthropic only | Costs |

Cloud providers expose spend through **AWS Cost Explorer, GCP Billing, or Azure Cost Management**. Claude for Teams and Enterprise plans include a usage dashboard at `claude.ai/analytics/claude-code`. The full Analytics, Monitoring usage, and Costs reference pages are digested elsewhere — see [Analytics](https://code.claude.com/docs/en/analytics), [Monitoring usage](https://code.claude.com/docs/en/monitoring-usage), and [Costs](https://code.claude.com/docs/en/costs).

## Review data handling

On Team, Enterprise, Claude API, and cloud-provider plans, Anthropic does not train models on your code or prompts. Your API provider determines retention and compliance posture.

| Topic | What to know | Where to start |
| :--- | :--- | :--- |
| Data usage policy | What Anthropic collects, how long it's retained, what's never used for training | Data usage |
| Zero Data Retention (ZDR) | Nothing stored after the request completes. Available to qualified accounts on Claude for Enterprise | Zero data retention |
| Security architecture | Network model, encryption, authentication, audit trail | Security |

If you need request-level audit logging or to route traffic by data sensitivity, place an [LLM gateway](https://code.claude.com/docs/en/llm-gateway) between developers and your provider. For regulatory requirements and certifications, see [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance). The data-usage, ZDR, security, and compliance reference pages are owned by the security/data cluster — linked, not duplicated here.

**Source**: https://code.claude.com/docs/en/admin-setup
**Last Updated**: 2026-06-13
**Status**: Active
