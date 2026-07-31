---
tags:
  - resource
  - documentation
  - claude_code
  - enterprise_deployment
  - deployment_options
keywords:
  - enterprise deployment overview
  - claude for teams
  - claude for enterprise
  - anthropic console
  - amazon bedrock
  - claude platform on aws
  - google vertex ai
  - microsoft foundry
  - deployment option comparison
topics:
  - Claude Code
  - Enterprise Deployment
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/third-party-integrations
access_control_group: ["general"]
---

# Claude Code — Enterprise Deployment Options

## Overview

Organizations can deploy Claude Code in one of two fundamental ways: **through Anthropic directly** or **through a cloud provider**. The enterprise-deployment-overview page exists to help an organization pick the right configuration, and for most organizations that choice is **Claude for Teams or Claude for Enterprise** — a single subscription gives team members both Claude Code and Claude on the web, with centralized billing and no infrastructure setup required.

Beyond the recommended Teams/Enterprise path, the page lays out six deployment options side by side — **Claude for Teams/Enterprise, Anthropic Console, Amazon Bedrock, Claude Platform on AWS, Google Vertex AI, and Microsoft Foundry** — so an organization with specific infrastructure requirements can compare them across best-for fit, billing, regions, prompt caching, authentication, cost tracking, web access, and enterprise features. This note digests that decision framing and the comparison; provider setup, proxy/gateway configuration, and org adoption best practices are linked out.

## Two Ways to Deploy

Organizations can deploy Claude Code through Anthropic directly or through a cloud provider. The page helps you choose the right configuration.

For most organizations, **Claude for Teams or Claude for Enterprise provides the best experience**. Team members get access to both Claude Code and Claude on the web with a single subscription, centralized billing, and no infrastructure setup required.

- **Claude for Teams** — self-service; includes collaboration features, admin tools, and billing management. Best for smaller teams that need to get started quickly.
- **Claude for Enterprise** — adds SSO and domain capture, role-based permissions, compliance API access, and managed policy settings for deploying organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.

If an organization has specific infrastructure requirements, it can instead deploy through a cloud provider and compare the options below.

## Compare Deployment Options

The page presents a six-column comparison table across eight feature rows. Summarized:

- **Best for** — Teams/Enterprise: most organizations (recommended). Anthropic Console: individual developers. Amazon Bedrock: AWS-native deployments. Claude Platform on AWS: AWS Marketplace billing with Claude API features. Google Vertex AI: GCP-native deployments. Microsoft Foundry: Azure-native deployments.
- **Billing** — Teams: $150/seat (Premium) with PAYG available; Enterprise: Contact Sales. Anthropic Console: PAYG. Amazon Bedrock: PAYG through AWS. Claude Platform on AWS: PAYG through AWS Marketplace. Google Vertex AI: PAYG through GCP. Microsoft Foundry: PAYG through Azure.
- **Regions** — Teams/Enterprise and Anthropic Console: supported countries. Amazon Bedrock and Claude Platform on AWS: multiple AWS regions. Google Vertex AI: multiple GCP regions. Microsoft Foundry: multiple Azure regions.
- **Prompt caching** — Enabled by default for every option.
- **Authentication** — Teams/Enterprise: Claude.ai SSO or email. Anthropic Console: API key. Amazon Bedrock and Claude Platform on AWS: API key or AWS credentials. Google Vertex AI: GCP credentials. Microsoft Foundry: API key or Microsoft Entra ID.
- **Cost tracking** — Teams/Enterprise and Anthropic Console: usage dashboard. Amazon Bedrock and Claude Platform on AWS: AWS Cost Explorer. Google Vertex AI: GCP Billing. Microsoft Foundry: Azure Cost Management.
- **Includes Claude on web** — Yes only for Teams/Enterprise; No for Anthropic Console, Amazon Bedrock, Claude Platform on AWS, Google Vertex AI, and Microsoft Foundry.
- **Enterprise features** — Teams/Enterprise: team management, SSO, usage monitoring. Anthropic Console: none. Amazon Bedrock and Claude Platform on AWS: IAM policies, CloudTrail. Google Vertex AI: IAM roles, Cloud Audit Logs. Microsoft Foundry: RBAC policies, Azure Monitor.

## Setup Pointers

Once an option is chosen, select it to view setup instructions:

- Claude for Teams or Enterprise → [cc_authentication](cc_authentication.md) (team-authentication section)
- Anthropic Console → [cc_authentication](cc_authentication.md) (Claude Console authentication)
- Amazon Bedrock → https://code.claude.com/docs/en/amazon-bedrock
- Claude Platform on AWS → https://code.claude.com/docs/en/claude-platform-on-aws
- Google Vertex AI → https://code.claude.com/docs/en/google-vertex-ai
- Microsoft Foundry → https://code.claude.com/docs/en/microsoft-foundry

For corporate proxy / LLM gateway configuration that may be layered on top of a cloud provider, see [cc_proxy_and_gateway_config](cc_proxy_and_gateway_config.md). For the org-wide adoption recommendations on the same page (documentation/memory, simplified install, guided usage, model pinning, managed security policies, central MCP), see https://code.claude.com/docs/en/third-party-integrations (Best practices for organizations). The administrator's end-to-end provider-selection flow is in [cc_admin_setup_decision_map](cc_admin_setup_decision_map.md).

**Source**: https://code.claude.com/docs/en/third-party-integrations
**Last Updated**: 2026-06-13
**Status**: Active
