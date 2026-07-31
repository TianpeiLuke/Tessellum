---
tags:
  - resource
  - documentation
  - claude_code
  - admin
  - deployment
keywords:
  - admin setup decision map
  - api provider selection
  - managed settings precedence
  - deployment decisions
  - choose api provider
  - verify and onboard
  - setting sources status
  - enterprise deployment
topics:
  - Claude Code
  - Administration
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/admin-setup
access_control_group: ["general"]
---

# Claude Code — Admin Setup Decision Map

## Overview

This page is the **administrator decision map** for deploying Claude Code across an organization. Claude Code enforces org policy through **managed settings** that take precedence over local developer configuration; an admin delivers those settings from the Claude admin console, a mobile device management (MDM) system, or a file on disk, and they control which tools, commands, servers, and network destinations Claude can reach. The page walks the deployment decisions in order, each row pointing to a deeper section and reference page.

The flow is five sequential decisions: **choose your API provider** (where Claude Code authenticates and how it's billed) → **decide how settings reach devices** (how managed policy reaches machines) → **decide what to enforce** (which tools/commands/integrations are allowed) → **set up usage visibility** (how spend and adoption are tracked) → **review data handling** (retention and compliance posture). This note covers the framing, the provider-selection decision, and the verify/onboard step; the enforcement catalog, settings-delivery precedence, deployment-option comparison, and authentication detail each live in their own sibling note.

## The Deployment Decision Table

The page lists the decisions in order; each row is a choice plus its reference:

| Decision | What you're choosing | Where it's covered |
| :--- | :--- | :--- |
| Choose your API provider | Where Claude Code authenticates and how it's billed | This note + [cc_enterprise_deployment_options](cc_enterprise_deployment_options.md) / [cc_authentication](cc_authentication.md) |
| Decide how settings reach devices | How managed policy reaches developer machines | [cc_server_managed_settings](cc_server_managed_settings.md) |
| Decide what to enforce | Which tools, commands, and integrations are allowed | [cc_admin_enforcement_controls](cc_admin_enforcement_controls.md) |
| Set up usage visibility | How you track spend and adoption | Analytics / [Monitoring](https://code.claude.com/docs/en/monitoring-usage) / Costs |
| Review data handling | Data retention and compliance posture | [Data usage](https://code.claude.com/docs/en/data-usage) / [Security](https://code.claude.com/docs/en/security) |

> **Note:** SSO, SCIM provisioning, and seat assignment are configured at the Claude account level (not via Claude Code's managed settings) — see the Claude Enterprise Administrator Guide and seat-assignment docs for those steps.

## Choose your API provider

Claude Code connects to Claude through one of several API providers. The choice affects billing, authentication, which compliance posture you inherit, and which Claude Code features developers can use.

| Provider | Choose this when |
| :--- | :--- |
| Claude for Teams / Enterprise | You want Claude Code and claude.ai under one per-seat subscription with no infrastructure to run. **This is the default recommendation.** |
| Claude Console | You're API-first or want pay-as-you-go billing |
| Amazon Bedrock | You want to inherit existing AWS compliance controls and billing |
| Google Vertex AI | You want to inherit existing GCP compliance controls and billing |
| Microsoft Foundry | You want to inherit existing Azure compliance controls and billing |

Some Claude Code features require a Claude.ai account. Claude Code on the web, Routines, Code Review, Remote Control, and the Chrome extension are **not** available through Console API keys or cloud-provider credentials alone. If you deploy through Bedrock, Vertex, or Foundry, plan whether developers also need Claude for Teams or Enterprise seats — each feature page lists its plan requirements.

The full provider comparison (authentication, regions, feature parity) is in [cc_enterprise_deployment_options](cc_enterprise_deployment_options.md); each provider's auth setup is in [cc_authentication](cc_authentication.md). Provider-specific deployment for [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), and [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) lives in those reference pages.

Proxy and firewall requirements apply regardless of provider (see [cc_proxy_and_gateway_config](cc_proxy_and_gateway_config.md) and [cc_network_tls_and_access](cc_network_tls_and_access.md)). If you want a single endpoint in front of multiple providers or centralized request logging, see [LLM gateway](https://code.claude.com/docs/en/llm-gateway).

## Verify and onboard

After configuring managed settings, have a developer run `/status` inside Claude Code. On the **Status** tab, the `Setting sources` line shows `Enterprise managed settings` followed by the source in parentheses — one of `(remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, or `(file)`. This confirms managed policy is reaching the device through the expected delivery mechanism.

Resources to share so developers get started: the Quickstart (first-session walkthrough from install to working with a project), Common workflows (patterns for code review, refactoring, debugging), and the self-paced Anthropic Academy courses (Claude 101, Claude Code in Action).

For login issues, point developers to [authentication troubleshooting](https://code.claude.com/docs/en/troubleshoot-install). The most common fixes are:

- Run `/logout` then `/login` to switch accounts.
- Run `claude update` if the enterprise auth option is missing.
- Restart the terminal after updating.

If a developer sees "You haven't been added to your organization yet," their seat doesn't include Claude Code access and needs to be updated in the admin console.

## Next steps

With provider and delivery mechanism chosen, the page routes to detailed configuration: [server-managed settings](cc_server_managed_settings.md) (deliver managed policy from the Claude admin console), the [Settings reference](https://code.claude.com/docs/en/settings) (every setting key, file location, and precedence rule), [Monorepos and large repos](https://code.claude.com/docs/en/large-codebases) (per-directory configuration for monorepos), provider-specific deployment for Bedrock / Vertex AI / Foundry, and the Claude Enterprise Administrator Guide (SSO, SCIM, seat management, and rollout playbook).

**Source**: https://code.claude.com/docs/en/admin-setup
**Last Updated**: 2026-06-13
**Status**: Active
