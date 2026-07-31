---
tags:
  - resource
  - documentation
  - claude_code
  - data_retention
  - enterprise
keywords:
  - zero data retention
  - zdr
  - claude for enterprise
  - real-time inference
  - per-organization enablement
  - features disabled under zdr
  - model availability under zdr
  - policy violation retention
topics:
  - Claude Code
  - Data & Compliance
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/zero-data-retention
access_control_group: ["general"]
---

# Claude Code — Zero Data Retention (ZDR)

## Overview

**Zero Data Retention (ZDR)** for Claude Code is available to qualified accounts on **Claude for Enterprise**. When ZDR is enabled, the prompts and model responses generated during Claude Code sessions are processed **in real time and not stored by Anthropic after the response is returned**, except where needed to comply with law or combat misuse. ZDR is *not* part of the standard Claude for Enterprise plan and cannot be turned on from admin settings — it is enabled separately by Anthropic for qualified accounts, on a per-organization basis.

Beyond the retention guarantee, ZDR on Claude for Enterprise also unlocks administrative capabilities: per-user cost controls, an analytics dashboard, server-managed settings, and audit logs. ZDR applies only to Anthropic's direct platform; deployments on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry follow those platforms' own data-retention policies.

## ZDR scope

ZDR covers **Claude Code inference on Claude for Enterprise**.

> **Per-organization enablement:** ZDR is enabled on a per-organization basis. Each new organization requires ZDR to be enabled separately by your Anthropic account team. ZDR does **not** automatically apply to new organizations created under the same account.

### What ZDR covers

ZDR covers model inference calls made through Claude Code on Claude for Enterprise. When you use Claude Code in your terminal, the prompts you send and the responses Claude generates are not retained by Anthropic. This applies to **every model available to ZDR organizations** — though some models require data retention and are therefore not available under ZDR (see [Model availability under ZDR](#model-availability-under-zdr)).

### What ZDR does not cover

ZDR does **not** extend to the following, even for organizations with ZDR enabled. These features instead follow standard data-retention policies (see [`cc_data_usage_and_telemetry`](cc_data_usage_and_telemetry.md), or the source [data-retention policy](https://code.claude.com/docs/en/data-usage)):

| Feature | Details |
|---------|---------|
| Chat on claude.ai | Chat conversations through the Claude for Enterprise web interface are not covered by ZDR. |
| Cowork | Cowork sessions are not covered by ZDR. |
| Claude Code Analytics | Does not store prompts or model responses, but collects productivity metadata such as account emails and usage statistics. Contribution metrics are not available for ZDR organizations; the analytics dashboard shows usage metrics only. |
| User and seat management | Administrative data such as account emails and seat assignments is retained under standard policies. |
| Third-party integrations | Data processed by third-party tools, MCP servers, or other external integrations is not covered by ZDR. Review those services' data handling practices independently. |

## Features disabled under ZDR

When ZDR is enabled for a Claude Code organization on Claude for Enterprise, certain features that require storing prompts or completions are **automatically disabled at the backend level**:

| Feature | Reason |
|---------|--------|
| Claude Code on the Web | Requires server-side storage of conversation history. |
| Cloud sessions from the Desktop app | Requires persistent session data that includes prompts and completions. |
| Feedback submission (`/feedback`) | Submitting feedback sends conversation data to Anthropic. |

These features are blocked in the backend regardless of client-side display. If a disabled feature appears in the Claude Code terminal during startup, attempting to use it returns an error indicating the organization's policies do not allow that action. Future features may also be disabled if they require storing prompts or completions.

### Model availability under ZDR

**Claude Fable 5 is not available** for organizations with zero data retention enabled. This model class requires data retention, so requests from ZDR organizations cannot be served by it. The model is either absent from the `/model` picker for ZDR organizations or shown as disabled with a notice that disabling ZDR is required, and the server rejects requests for it regardless of client configuration.

Other models remain available under ZDR. Fable 5 is not the default model, and the `best` alias — which resolves to Fable 5 where it is available — resolves to **Opus** for organizations where it is not, including ZDR organizations.

## Data retention for policy violations

Even with ZDR enabled, Anthropic may retain data where required by law or to address **Usage Policy violations**. If a session is flagged for a policy violation, Anthropic may retain the associated inputs and outputs for **up to 2 years**, consistent with Anthropic's standard ZDR policy.

## Request ZDR

To request ZDR for Claude Code on Claude for Enterprise, contact sales or your Anthropic account team. Your account team submits the request internally, and Anthropic reviews and enables ZDR on your organization after confirming eligibility. **All enablement actions are audit-logged.**

If you are currently using ZDR for Claude Code via pay-as-you-go API keys, you can transition to Claude for Enterprise to gain access to administrative features while maintaining ZDR for Claude Code. Contact your account team to coordinate the migration.

**Source**: https://code.claude.com/docs/en/zero-data-retention
**Last Updated**: 2026-06-13
**Status**: Active
