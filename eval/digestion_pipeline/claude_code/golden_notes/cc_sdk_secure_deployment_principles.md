---
tags:
  - resource
  - documentation
  - claude_code
  - secure_deployment
  - security
keywords:
  - secure agent deployment
  - prompt injection threat model
  - built-in security features
  - permissions system
  - security boundary
  - least privilege
  - defense in depth
  - semi-trusted code
topics:
  - Claude Code
  - Agent SDK Security
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/agent-sdk/secure-deployment
access_control_group: ["general"]
---

# SDK Secure Deployment — Security Principles

## Overview

Claude Code and the Agent SDK can execute code, access files, and interact with external services. Unlike traditional software that follows predetermined code paths, these tools **generate their actions dynamically based on context and goals**. That flexibility is what makes them useful, but it also means their behavior can be influenced by the content they process — files, webpages, or user input. The core security argument of this guide is that an agent is best treated as **semi-trusted code**, so the same principles that apply to running any semi-trusted code apply here: **isolation, least privilege, and defense in depth**.

Securing an agent deployment does not require exotic infrastructure. Not every deployment needs maximum security — a developer running Claude Code on a laptop has different requirements than a company processing customer data in a multi-tenant environment. This note covers the threat model that motivates hardening, the built-in security features Claude Code ships with, and the three principles that guide the available options. The concrete mechanisms (isolation technologies, credential proxying, filesystem controls) are documented in the sibling notes.

## Threat model

Agents can take unintended actions due to **prompt injection** (instructions embedded in content they process) or **model error**. For example, if a repository's README contains unusual instructions, Claude Code might incorporate those into its actions in ways the operator did not anticipate. Claude models are designed to resist this; the [model overview](https://platform.claude.com/docs/en/about-claude/models/overview) and the system card for the deployed model cover evaluation details.

Defense in depth is still good practice. The motivating example: if an agent processes a malicious file that instructs it to send customer data to an external server, **network controls can block that request entirely** — even if the model is influenced, an independent control layer contains the damage.

## Built-in security features

Claude Code includes several security features that address common concerns (full details in the [security documentation](https://code.claude.com/docs/en/security)):

- **Permissions system** — Every tool and bash command can be configured to allow, block, or prompt the user for approval. Glob patterns create rules like "allow all npm commands" or "block any command with sudo". Organizations can set policies that apply across all users. See [permissions](https://code.claude.com/docs/en/permissions).
- **Command parsing for permissions** — Before executing bash commands, Claude Code parses them into an AST and matches the result against your permission rules. Commands that cannot be parsed cleanly, or that do not match an allow rule, require explicit approval. A small set of constructs such as `eval` always require approval regardless of allow rules. This is a **permission gate, not a sandbox**; it does not infer whether a command is dangerous from its target path or effects.
- **Web search summarization** — Search results are summarized rather than passing raw content directly into the context, reducing the risk of prompt injection from malicious web content.
- **Sandbox mode** — Bash commands can run in a sandboxed environment that restricts filesystem and network access. See the [sandboxing documentation](https://code.claude.com/docs/en/sandboxing) for details.

## Security principles

For deployments that require hardening beyond Claude Code's defaults, three principles guide the available options.

### Security boundaries

A **security boundary** separates components with different trust levels. For high-security deployments, you can place sensitive resources (like credentials) *outside* the boundary containing the agent. If something goes wrong in the agent's environment, resources outside that boundary remain protected.

The recurring example: rather than giving an agent direct access to an API key, run a **proxy outside the agent's environment** that injects the key into requests. The agent can make API calls, but it never sees the credential itself. This pattern is useful for multi-tenant deployments or when processing untrusted content (see [SDK Credential and Filesystem Controls](cc_sdk_credential_and_filesystem_controls.md) for the implementation).

### Least privilege

When needed, restrict the agent to only the capabilities required for its specific task:

| Resource            | Restriction options                             |
| ------------------- | ----------------------------------------------- |
| Filesystem          | Mount only needed directories, prefer read-only |
| Network             | Restrict to specific endpoints via proxy        |
| Credentials         | Inject via proxy rather than exposing directly  |
| System capabilities | Drop Linux capabilities in containers           |

### Defense in depth

For high-security environments, **layering multiple controls** provides additional protection. Options include:

- Container isolation
- Network restrictions
- Filesystem controls
- Request validation at a proxy

The right combination depends on your threat model and operational requirements. The concrete isolation strength/overhead/complexity tradeoffs are catalogued in [SDK Isolation Technologies](cc_sdk_isolation_technologies.md), and the credential-proxy and filesystem mechanics in [SDK Credential and Filesystem Controls](cc_sdk_credential_and_filesystem_controls.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/secure-deployment
**Last Updated**: 2026-06-13
**Status**: Active
