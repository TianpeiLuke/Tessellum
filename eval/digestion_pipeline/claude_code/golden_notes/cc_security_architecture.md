---
tags:
  - resource
  - documentation
  - claude_code
  - security
  - architecture
keywords:
  - security architecture
  - read-only permissions by default
  - permission-based architecture
  - built-in protections
  - sandboxed bash tool
  - write access restriction
  - accept edits mode
  - mcp security
  - user responsibility
  - team security
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

# Claude Code — Security Architecture

## Overview

Claude Code is built with security at its core and developed according to Anthropic's comprehensive security program, whose certifications (SOC 2 Type 2 report, ISO 27001 certificate, etc.) are published at the Anthropic Trust Center. Its security model rests on a **permission-based architecture**: Claude Code uses strict read-only permissions by default, and any action that could modify the system requires explicit approval. On top of those permissions sit four built-in protections that mitigate the risks of agentic systems, a trust model for MCP servers configured in source control, and best practices for teams and sensitive repositories.

This note covers the security *foundation*, the *permission architecture*, the *built-in protections*, *user responsibility*, *MCP security*, and *team/sensitive-code* best practices. Detailed permission configuration, sandbox tuning, and usage monitoring are owned by separate pages and linked out below; the prompt-injection defenses on the same source page and the in-session vulnerability-review plugin are linked out in the Related Notes section.

## Security foundation

Your code's security is paramount. Claude Code is built with security at its core, developed according to Anthropic's comprehensive security program. Resources including the SOC 2 Type 2 report and ISO 27001 certificate are available at the [Anthropic Trust Center](https://trust.anthropic.com).

## Permission-based architecture

Claude Code uses **strict read-only permissions by default**. When additional actions are needed (editing files, running tests, executing commands), Claude Code requests explicit permission. Users control whether to approve actions once or allow them automatically.

Claude Code requires approval before running Bash commands that can modify your system. A built-in set of read-only commands such as `ls`, `cat`, and `git status` runs without a prompt. This approach lets users and organizations configure permissions directly. For detailed permission configuration, see [Permissions](https://code.claude.com/docs/en/permissions).

## Built-in protections

To mitigate risks in agentic systems, Claude Code provides four built-in protections:

- **Sandboxed bash tool** — sandboxes bash commands with filesystem and network isolation, reducing permission prompts while maintaining security. Enabled with `/sandbox` to define boundaries where Claude Code can work autonomously (see [Sandboxing](https://code.claude.com/docs/en/sandboxing)).
- **Write access restriction** — Claude Code can only write to the folder where it was started and its subfolders; it cannot modify files in parent directories without explicit permission. It *can read* files outside the working directory (useful for accessing system libraries and dependencies), but write operations are strictly confined to the project scope, creating a clear security boundary.
- **Prompt fatigue mitigation** — support for allowlisting frequently used safe commands per-user, per-codebase, or per-organization.
- **Accept Edits mode** — auto-approves file edits and a fixed set of filesystem Bash commands like `mkdir`, `touch`, `rm`, `mv`, `cp`, and `sed` for paths in the working directory. Other Bash commands and out-of-scope paths still prompt.

## User responsibility

Claude Code only has the permissions you grant it. You are responsible for reviewing proposed code and commands for safety before approval.

## MCP security

Claude Code allows users to configure Model Context Protocol (MCP) servers. The list of allowed MCP servers is configured in your source code, as part of Claude Code settings that engineers check into source control.

Anthropic encourages either writing your own MCP servers or using MCP servers from providers that you trust. You are able to configure Claude Code permissions for MCP servers. Anthropic reviews connectors against its listing criteria before adding them to the Anthropic Directory, but does not security-audit or manage any MCP server.

## Cloud and IDE execution

When running Claude Code in an IDE or in the cloud, additional security controls apply. Running in VS Code is covered in [VS Code security and privacy](https://code.claude.com/docs/en/vs-code#security-and-privacy). Cloud execution security (isolated VMs, network access controls, scoped credential proxy, branch restrictions, audit logging, and automatic cleanup) and the local-only Remote Control connection are documented with the data-flow details in [`cc_data_usage_and_telemetry`](cc_data_usage_and_telemetry.md) and on the [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) page.

## Security best practices

### Working with sensitive code

- Review all suggested changes before approval.
- Use project-specific permission settings for sensitive repositories.
- Consider using [dev containers](https://code.claude.com/docs/en/devcontainer) for additional isolation.
- Regularly audit your permission settings with `/permissions`.

### Team security

- Use [managed settings](https://code.claude.com/docs/en/settings#settings-files) to enforce organizational standards.
- Share approved permission configurations through version control.
- Train team members on security best practices.
- Monitor Claude Code usage through [OpenTelemetry metrics](https://code.claude.com/docs/en/monitoring-usage).
- Audit or block settings changes during sessions with [`ConfigChange` hooks](https://code.claude.com/docs/en/hooks#configchange).

### Reporting security issues

Security vulnerabilities should be reported privately through Anthropic's HackerOne program rather than disclosed publicly; the reporting procedure is documented in [`cc_legal_and_compliance`](cc_legal_and_compliance.md).

**Source**: https://code.claude.com/docs/en/security
**Last Updated**: 2026-06-13
**Status**: Active
