---
tags:
  - resource
  - terminology
  - security
  - agentic_ai
  - developer_tools
keywords:
  - tirith
  - pre-exec security scanning
  - content-level command scanning
  - homograph URL spoofing
  - pipe-to-interpreter
  - terminal injection
  - pre-execution gate
  - command scanner
topics:
  - Security
  - Agentic AI
  - Command Execution Safety
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Tirith - Pre-Exec Security Scanner

## Definition

**Tirith** is an open-source, content-level **pre-execution security scanner** that inspects shell commands, pasted content, and files *before* they run — catching threats that simple pattern-matching allowlists/denylists miss. Its design premise is that a browser would flag a malicious URL or script but a terminal (or an autonomous coding agent driving one) will execute the same input without scrutiny. Tirith closes that gap by acting as a gate between the request to run a command and the command actually executing, returning a structured verdict (safe / suspicious / blocked) with a severity, a human-readable finding, and a safer alternative.

Tirith matters as one of the layers in the **defense-in-depth** model of the **[Hermes Agent](term_autonomous_coding_agents.md)** harness: Hermes integrates Tirith for content-level command scanning, and Tirith's verdict feeds the harness's command-approval flow. Where Hermes' built-in dangerous-pattern denylist matches on coarse string patterns, Tirith analyzes command *structure* — Unicode lookalikes, source-to-sink pipe chains, and escape-sequence injection — to detect attacks that survive naive pattern matching. It is the concrete tool that implements the threat *defense*, as distinct from the abstract threat classes (adversarial attacks, prompt injection) it defends against.

## Context

- **Hermes Agent harness.** Tirith is wired into Hermes' `## Tirith Pre-Exec Security Scanning` layer (security model). It is enabled by default via `security.tirith_enabled: true` in `~/.hermes/config.yaml`, with knobs for the binary `tirith_path`, a subprocess `tirith_timeout` (default 5s), and a `tirith_fail_open` flag (default `true`) that lets commands proceed if the scanner is missing or times out — set `false` in high-security environments to fail closed.
- **Approval-flow integration.** A *safe* verdict passes through silently; both *suspicious* and *blocked* verdicts trigger user approval, surfacing the full Tirith finding (severity, title, description, safer alternative). The default choice is **deny**, keeping unattended/headless scenarios secure.
- **Cross-platform availability.** Prebuilt binaries ship for Linux (x86_64 / aarch64) and macOS (x86_64 / arm64). On platforms with no prebuilt binary (e.g. native Windows) Tirith is silently skipped — pattern-matching guards still run — and the recommendation is to run the agent under WSL to regain Tirith coverage.
- **Supply-chain hygiene.** Tirith auto-installs from GitHub releases on first use, verified by SHA-256 checksum (plus cosign provenance verification when cosign is available) — itself an example of the supply-chain integrity controls it also helps enforce on the commands it scans.

## Key Characteristics

- **Structure-based, pre-execution analysis** — inspects the *structure* of commands/content/files rather than runtime behavior; it is explicitly not antivirus or a runtime sandbox, and runs as a per-command gate (no resident daemon by default).
- **Threat classes detected** — homograph / internationalized-domain URL spoofing (Cyrillic/Greek lookalikes, punycode, mixed-script labels), pipe-to-interpreter source-to-sink chains (`curl | bash`, `wget | sh`), terminal-injection attacks (ANSI escape sequences, bidi overrides, zero-width / invisible characters), plus base64 decode-execute chains, data exfiltration, and supply-chain threats (typosquats, known-bad packages).
- **Severity-graded verdicts** — findings are graded CRITICAL / HIGH / MEDIUM / LOW and resolve to BLOCKED, WARNING, or silent-pass (e.g. a homograph URL is CRITICAL and blocked; a clean pipe-to-shell is MEDIUM and only warned).
- **Explainable findings** — each verdict carries a title, description, and a safer alternative, which Hermes forwards into the approval prompt so a human can make an informed approve/deny decision.
- **Agent-callable** — exposes an MCP server so an AI agent can request a check before acting, in addition to the shell-hook and file/directory/config scanning entry points.
- **Verified, no-telemetry distribution** — implemented primarily in Rust with sub-millisecond per-command overhead; releases are checksum- and cosign-verifiable (`tirith verify-self`), detection runs local-only with no telemetry, and a signed local threat database is refreshed on a schedule.

## Related Terms


## References

- [Hermes Agent — Security: Tirith Pre-Exec Security Scanning](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- [tirith — GitHub repository (sheeki03/tirith)](https://github.com/sheeki03/tirith)
- [OWASP — Improper Neutralization / Argument Injection (pipe-to-shell, command-injection guidance)](https://owasp.org/www-community/attacks/Command_Injection)
- [Unicode Technical Report #36 — Unicode Security Considerations (homograph / confusable detection)](https://www.unicode.org/reports/tr36/)

---

**Last Updated**: 2026-06-19
**Status**: Active
