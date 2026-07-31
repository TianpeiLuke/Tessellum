---
tags:
  - resource
  - documentation
  - claude_code
  - enterprise
  - best_practices
keywords:
  - best practices for organizations
  - invest in documentation and memory
  - simplify deployment
  - start with guided usage
  - pin model versions
  - configure security policies
  - leverage mcp for integrations
  - org-wide claude.md
  - guided usage ramp
  - rollout next steps
topics:
  - Claude Code
  - Enterprise
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/third-party-integrations
access_control_group: ["general"]
---

# Claude Code — Enterprise Adoption Best Practices

## Overview

The core claim of this note is that **a successful organization-wide Claude Code rollout is not just a deployment-option choice — it requires deliberate investment in documentation, frictionless installation, a graduated usage ramp, version control, security policy, and shared integrations.** Anthropic's recommendation is that organizations who give Claude Code the context it needs (CLAUDE.md), the lowest-friction install path, and centrally-managed configuration get the most value, while users who start small and let Claude run more agentically over time become more effective. The page presents six adoption recommendations and a three-step rollout sequence; the deeper mechanics of each (memory, model pinning, permissions, MCP) live on their dedicated pages and are linked out rather than re-explained here.

## Best practices for organizations

The docs give six recommendations for organizations adopting Claude Code.

### Invest in documentation and memory

Anthropic "strongly recommend[s] investing in documentation so that Claude Code understands your codebase." Organizations can deploy `CLAUDE.md` files at multiple levels:

- **Organization-wide**: Deploy to system directories like `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) for company-wide standards.
- **Repository-level**: Create `CLAUDE.md` files in repository roots containing project architecture, build commands, and contribution guidelines. Check these into source control so all users benefit.

Full mechanics of memory files are documented in [Memory and CLAUDE.md files](https://code.claude.com/docs/en/memory).

### Simplify deployment

For organizations with a custom development environment, the source finds that creating a "one click" way to install Claude Code is key to growing adoption across the organization.

### Start with guided usage

Encourage new users to try Claude Code for codebase Q&A, or on smaller bug fixes or feature requests. Ask Claude Code to make a plan, check its suggestions, and give feedback if it's off-track. Per the source: "Over time, as users understand this new paradigm better, then they'll be more effective at letting Claude Code run more agentically." The ramp moves users from supervised, small-scope tasks toward more autonomous operation as trust builds.

### Pin model versions for cloud providers

If you deploy through Bedrock, Vertex AI, Foundry, or Claude Platform on AWS, pin specific model versions using `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Without pinning, model aliases resolve to Claude Code's built-in default for that provider, which can lag the newest release and may not yet be enabled in your account. Pinning lets you control when your users move to a new model. See [Model configuration](https://code.claude.com/docs/en/model-config) for what each provider does when the default is unavailable.

### Configure security policies

Security teams can configure managed permissions for what Claude Code is and is not allowed to do, which cannot be overwritten by local configuration. The full security/permissions surface is documented in [Security](https://code.claude.com/docs/en/security).

### Leverage MCP for integrations

MCP is "a great way to give Claude Code more information, such as connecting to ticket management systems or error logs." The recommendation is that **one central team configures MCP servers and checks a `.mcp.json` configuration into the codebase** so that all users benefit. Full MCP setup is documented in [MCP](https://code.claude.com/docs/en/mcp).

The section closes with Anthropic's own endorsement: it trusts Claude Code to power development across every Anthropic codebase.

## Next steps

Once you've chosen a deployment option (see [cc_enterprise_deployment_options](cc_enterprise_deployment_options.md)) and configured access for your team, the source gives a three-step rollout sequence:

1. **Roll out to your team** — Share installation instructions and have team members install Claude Code and authenticate with their credentials.
2. **Set up shared configuration** — Create a `CLAUDE.md` file in your repositories to help Claude Code understand your codebase and coding standards.
3. **Configure permissions** — Review security settings to define what Claude Code can and cannot do in your environment.

**Source**: https://code.claude.com/docs/en/third-party-integrations
**Last Updated**: 2026-06-13
**Status**: Active
