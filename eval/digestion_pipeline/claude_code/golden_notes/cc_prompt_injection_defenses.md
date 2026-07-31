---
tags:
  - resource
  - documentation
  - claude_code
  - security
  - prompt_injection
keywords:
  - prompt injection
  - core protections
  - additional safeguards
  - network command approval
  - isolated context window
  - command injection detection
  - fail-closed matching
  - working with untrusted content
topics:
  - Claude Code
  - Security
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/security
access_control_group: ["general"]
---

# Claude Code — Prompt Injection Defenses

## Overview

**Prompt injection** is a technique where an attacker attempts to override or manipulate an AI assistant's instructions by inserting malicious text into content the model reads. Because Claude Code is an agentic tool that can run commands, edit files, and fetch from the web, an injected instruction could attempt to trigger real actions rather than merely altering text — so the security page documents a layered set of safeguards specifically against these attacks.

This note covers Claude Code's prompt-injection-specific defenses: the **core protections**, a pointer to the **privacy safeguards**, the **additional safeguards** (including the Windows WebDAV warning), and the **best practices for working with untrusted content**. The broader permission/sandbox/MCP security model that these defenses build on is in [Security Architecture](cc_security_architecture.md). For the generic concept itself, see the [Prompt Injection](../../term_dictionary/term_prompt_injection.md) term note.

## Core protections

Claude Code includes several safeguards against prompt-injection attacks:

- **Permission system** — sensitive operations require explicit approval.
- **Context-aware analysis** — detects potentially harmful instructions by analyzing the full request.
- **Input sanitization** — prevents command injection by processing user inputs.
- **Network command approval** — commands that fetch content from the web such as `curl` and `wget` are not auto-approved by default. They prompt like any other non-read-only Bash command, so you can still approve once or add an explicit allow rule like `Bash(curl *)`. To block them entirely, add them to [`permissions.deny`](https://code.claude.com/docs/en/permissions#tool-specific-permission-rules).

## Privacy safeguards (pointer)

The security page also lists privacy safeguards — limited retention periods for sensitive information, restricted access to user session data, and user control over data-training preferences (consumer users can change their privacy settings at any time). These are summarized here only as a pointer; the full data-usage and retention policy is documented in [Data Usage & Telemetry](cc_data_usage_and_telemetry.md), and the governing legal terms in [Legal & Compliance](cc_legal_and_compliance.md).

## Additional safeguards

- **Network request approval** — tools that make network requests require user approval by default.
- **Isolated context windows** — web fetch uses a separate context window to avoid injecting potentially malicious prompts.
- **Trust verification** — first-time codebase runs and new MCP servers require trust verification.
  - Trust verification is disabled when running non-interactively with the `-p` flag.
  - When you start Claude Code directly in your home directory, trust acceptance is held for the current session only and is not written to disk, so the prompt reappears on each launch. There is no setting to persist it; start Claude Code from a project subdirectory instead, where trust acceptance is saved per directory.
- **Command injection detection** — suspicious bash commands require manual approval even if previously allowlisted.
- **Fail-closed matching** — unmatched commands default to requiring manual approval.
- **Natural language descriptions** — complex bash commands include explanations for user understanding.
- **Secure credential storage** — API keys and tokens are stored in the macOS Keychain when available, and protected by file permissions on Windows and Linux. (Credential-management detail is covered under authentication: `https://code.claude.com/docs/en/authentication#credential-management`.)

**Windows WebDAV security risk**: When running Claude Code on Windows, Anthropic recommends *against* enabling WebDAV or allowing Claude Code to access paths such as `\\*` that may contain WebDAV subdirectories. WebDAV has been deprecated by Microsoft due to security risks. Enabling WebDAV may allow Claude Code to trigger network requests to remote hosts, bypassing the permission system.

## Best practices for working with untrusted content

1. Review suggested commands before approval.
2. Avoid piping untrusted content directly to Claude.
3. Verify proposed changes to critical files.
4. Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services.
5. Report suspicious behavior with `/feedback`.

While these protections significantly reduce risk, **no system is completely immune to all attacks**. Always maintain good security practices when working with any AI tool.

**Source**: https://code.claude.com/docs/en/security
**Last Updated**: 2026-06-13
**Status**: Active
