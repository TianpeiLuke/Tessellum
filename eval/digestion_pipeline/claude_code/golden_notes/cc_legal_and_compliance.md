---
tags:
  - resource
  - documentation
  - claude_code
  - legal_compliance
  - governance
keywords:
  - legal agreements
  - commercial terms
  - consumer terms
  - business associate agreement
  - baa healthcare compliance
  - acceptable use policy
  - oauth vs api key authentication
  - trust center
  - hackerone vulnerability reporting
  - agent sdk credit
topics:
  - Claude Code
  - Legal & Compliance
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/legal-and-compliance
access_control_group: ["general"]
---

# Claude Code — Legal and Compliance

## Overview

This note documents the legal agreements, compliance certifications, usage policy, and security/trust resources that govern Claude Code use. It covers which terms apply by plan type (Commercial vs Consumer), how existing 1P/3P commercial agreements carry over, the conditions under which a healthcare **Business Associate Agreement (BAA)** extends to Claude Code, the Acceptable Use Policy, the boundary between **OAuth** and **API key** authentication, and where to find trust resources and report vulnerabilities.

A scheduling note also applies: starting **June 15, 2026**, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from interactive usage limits.

## Legal agreements

### License

Use of Claude Code is subject to one of two agreements depending on plan type:

- **[Commercial Terms](https://www.anthropic.com/legal/commercial-terms)** — for Team, Enterprise, and Claude API users.
- **[Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms)** — for Free, Pro, and Max users.

### Commercial agreements

Whether you use the Claude API directly (1P) or access it through Amazon Bedrock or Google Vertex (3P), your existing commercial agreement applies to Claude Code usage, unless Anthropic has mutually agreed otherwise.

## Compliance

### Healthcare compliance (BAA)

If a customer has a **Business Associate Agreement (BAA)** with Anthropic and wants to use Claude Code, the BAA automatically extends to cover Claude Code provided the customer has both executed a BAA and has [Zero Data Retention (ZDR)](cc_zero_data_retention.md) activated. The BAA applies to that customer's API traffic flowing through Claude Code. ZDR is enabled on a **per-organization** basis, so each organization must have ZDR enabled separately to be covered under the BAA.

## Usage policy

### Acceptable use

Claude Code usage is subject to the [Anthropic Usage Policy](https://www.anthropic.com/legal/aup). Advertised usage limits for Pro and Max plans **assume ordinary, individual usage** of Claude Code and the Agent SDK.

### Authentication and credential use

Claude Code authenticates with Anthropic's servers using **OAuth tokens** or **API keys**. These methods serve different purposes:

- **OAuth authentication** is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans, and is designed to support ordinary use of Claude Code and other native Anthropic applications.
- **Developers** building products or services that interact with Claude's capabilities — including those using the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) — should use API key authentication through the Claude Console or a supported cloud provider. Anthropic does **not** permit third-party developers to offer Claude.ai login or to route requests through Free, Pro, or Max plan credentials on behalf of their users.

Anthropic reserves the right to take measures to enforce these restrictions and may do so without prior notice. For questions about permitted authentication methods, the docs direct users to contact sales.

## Security and trust

### Trust and safety

More information is available in the [Anthropic Trust Center](https://trust.anthropic.com) and the [Transparency Hub](https://www.anthropic.com/transparency).

### Security vulnerability reporting

Anthropic manages its security program through **HackerOne**; vulnerabilities are reported via the [HackerOne form](https://hackerone.com/4f1f16ba-10d3-4d09-9ecc-c721aad90f24/embedded_submissions/new). The security guidance for reporting a discovered Claude Code vulnerability is to: not disclose it publicly, report it through the HackerOne program, include detailed reproduction steps, and allow time for Anthropic to address the issue before public disclosure.

**Source**: https://code.claude.com/docs/en/legal-and-compliance
**Last Updated**: 2026-06-13
**Status**: Active
