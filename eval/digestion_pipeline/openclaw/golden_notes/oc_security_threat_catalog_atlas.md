---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - threat_model
keywords:
  - openclaw threat catalog
  - mitre atlas tactic threats
  - prompt injection threat
  - exec approval bypass
  - credential harvesting skill
  - ssrf web_fetch exfiltration
  - aml technique mapping
  - residual risk mitigation
topics:
  - OpenClaw
  - Security Threat Catalog
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS
access_control_group: ["general"]
---

# OpenClaw — Threat Catalog by MITRE ATLAS Tactic

## Overview

This note is the per-tactic threat catalog of OpenClaw's MITRE-ATLAS threat model — the argument that OpenClaw enumerates ~22 distinct adversarial threats (each a `T-*` ID) across eight ATLAS tactics, and for each threat asserts a specific attack vector, affected components, the mitigation in place today, and the *residual risk* that remains after that mitigation. It mirrors `security/THREAT-MODEL-ATLAS.md` §3 (Threat Analysis by ATLAS Tactic, 3.1 Reconnaissance → 3.8 Impact), §7.1 (the AML.T0xxx → `T-*` technique mapping), and §7.3 (the glossary). The companion architecture model (the five trust boundaries) and the ClawHub supply-chain / risk-matrix / recommendations notes are split out as siblings.

The recurring claim across every entry is the gap between *detection* and *blocking*: many of OpenClaw's "Current Mitigations" are advisory (pattern detection, content wrapping, exec-approval *ask* mode, file permissions) rather than enforcing, so the documented residual risk stays **Critical** or **High** for the threats that compose the catalog's published attack chains.

## §3 Threat Analysis by ATLAS Tactic

Each threat is recorded with the same attributes in source: ATLAS ID, Description, Attack Vector, Affected Components, Current Mitigations, Residual Risk, Recommendations. The catalog is organized by the eight ATLAS tactics below; threat IDs are namespaced by tactic (`T-RECON-*`, `T-ACCESS-*`, etc.).

### 3.1 Reconnaissance (AML.TA0002)

- **T-RECON-001 Agent Endpoint Discovery** (AML.T0006 Active Scanning) — attacker scans for exposed gateway endpoints via network scanning, shodan queries, DNS enumeration; affects the Gateway / exposed API endpoints. Current mitigations: Tailscale auth option, bind to loopback by default. Residual risk **Medium** (public gateways discoverable). Recommends documenting secure deployment and rate limiting on discovery endpoints.
- **T-RECON-002 Channel Integration Probing** (AML.T0006 Active Scanning) — attacker probes messaging channels to identify AI-managed accounts by sending test messages and observing response patterns; affects all channel integrations. Current mitigations: **None specific**. Residual risk **Low** (limited value from discovery alone). Recommends response timing randomization.

### 3.2 Initial Access (AML.TA0004)

All three Initial-Access threats map to AML.T0040 (AI Model Inference API Access).

- **T-ACCESS-001 Pairing Code Interception** — attacker intercepts a pairing code during the pairing grace period (**1h for DM channel pairing, 5m for node pairing**) via shoulder surfing, network sniffing, or social engineering; affects the device pairing system. Current mitigations: 1h expiry (DM pairing) / 5m expiry (node pairing), codes sent via the existing channel. Residual risk **Medium** (grace period exploitable). Recommends reducing the grace period and adding a confirmation step.
- **T-ACCESS-002 AllowFrom Spoofing** — attacker spoofs an allowed sender identity in a channel (phone-number spoofing, username impersonation, channel-dependent); affects per-channel `AllowFrom` validation. Current mitigations: channel-specific identity verification. Residual risk **Medium** (some channels vulnerable to spoofing). Recommends documenting channel-specific risks and adding cryptographic verification where possible.
- **T-ACCESS-003 Token Theft** — attacker steals authentication tokens from config files via malware, unauthorized device access, or config-backup exposure; affects `~/.openclaw/credentials/` and config storage. Current mitigations: file permissions. Residual risk **High** (tokens stored in plaintext). Recommends token encryption at rest and token rotation.

### 3.3 Execution (AML.TA0005)

This tactic is where prompt injection lives and is the catalog's highest-severity cluster.

- **T-EXEC-001 Direct Prompt Injection** (AML.T0051.000 LLM Prompt Injection: Direct) — attacker sends crafted prompts to manipulate agent behavior via channel messages containing adversarial instructions; affects the agent LLM and all input surfaces. Current mitigations: pattern detection, external content wrapping. Residual risk **Critical** — *"Detection only, no blocking; sophisticated attacks bypass."* Recommends multi-layer defense, output validation, and user confirmation for sensitive actions.
- **T-EXEC-002 Indirect Prompt Injection** (AML.T0051.001 LLM Prompt Injection: Indirect) — attacker embeds malicious instructions in fetched content via malicious URLs, poisoned emails, or compromised webhooks; affects `web_fetch`, email ingestion, and external data sources. Current mitigations: content wrapping with XML tags and a security notice. Residual risk **High** (the LLM may ignore wrapper instructions). Recommends content sanitization and separate execution contexts.
- **T-EXEC-003 Tool Argument Injection** (AML.T0051.000 LLM Prompt Injection: Direct) — attacker manipulates tool arguments through prompt injection, using crafted prompts that influence tool parameter values; affects all tool invocations. Current mitigations: exec approvals for dangerous commands. Residual risk **High** (relies on user judgment). Recommends argument validation and parameterized tool calls.
- **T-EXEC-004 Exec Approval Bypass** (AML.T0043 Craft Adversarial Data) — attacker crafts commands that bypass the approval allowlist via command obfuscation, alias exploitation, or path manipulation; affects `exec-approvals.ts` and the command allowlist. Current mitigations: allowlist + ask mode. Residual risk **High** (no command sanitization). Recommends command normalization and an expanded blocklist.

### 3.4 Persistence (AML.TA0006)

- **T-PERSIST-001 Malicious Skill Installation** (AML.T0010.001 Supply Chain Compromise: AI Software) — attacker publishes a malicious skill to ClawHub by creating an account and hiding malicious code; affects ClawHub, skill loading, and agent execution. Current mitigations: GitHub account-age verification, pattern-based moderation flags. Residual risk **Critical** (no sandboxing, limited review). Recommends VirusTotal integration (in progress), skill sandboxing, and community review.
- **T-PERSIST-002 Skill Update Poisoning** (AML.T0010.001 Supply Chain Compromise: AI Software) — attacker compromises a popular skill and pushes a malicious update via account compromise or social engineering of the skill owner; affects ClawHub versioning and auto-update flows. Current mitigations: version fingerprinting. Residual risk **High** (auto-updates may pull malicious versions). Recommends update signing, rollback capability, and version pinning.
- **T-PERSIST-003 Agent Configuration Tampering** (AML.T0010.002 Supply Chain Compromise: Data) — attacker modifies agent configuration to persist access via config-file modification or settings injection; affects agent config and tool policies. Current mitigations: file permissions. Residual risk **Medium** (requires local access). Recommends config integrity verification and audit logging for config changes.

### 3.5 Defense Evasion (AML.TA0007)

Both Defense-Evasion threats map to AML.T0043 (Craft Adversarial Data).

- **T-EVADE-001 Moderation Pattern Bypass** — attacker crafts skill content to evade moderation patterns using Unicode homoglyphs, encoding tricks, or dynamic loading; affects ClawHub `moderation.ts`. Current mitigations: pattern-based `FLAG_RULES`. Residual risk **High** (simple regex easily bypassed). Recommends behavioral analysis (VirusTotal Code Insight) and AST-based detection.
- **T-EVADE-002 Content Wrapper Escape** — attacker crafts content that escapes the XML-wrapper context via tag manipulation, context confusion, or instruction override; affects external content wrapping. Current mitigations: XML tags + security notice. Residual risk **Medium** (novel escapes discovered regularly). Recommends multiple wrapper layers and output-side validation.

### 3.6 Discovery (AML.TA0008)

Both Discovery threats map to AML.T0040 (AI Model Inference API Access).

- **T-DISC-001 Tool Enumeration** — attacker enumerates available tools through prompting (`"What tools do you have?"`-style queries); affects the agent tool registry. Current mitigations: **None specific**. Residual risk **Low** (tools generally documented). Recommends considering tool-visibility controls.
- **T-DISC-002 Session Data Extraction** — attacker extracts sensitive data from session context via `"What did we discuss?"` queries and context probing; affects session transcripts and the context window. Current mitigations: session isolation per sender. Residual risk **Medium** (within-session data accessible). Recommends sensitive-data redaction in context.

### 3.7 Collection & Exfiltration (AML.TA0009, AML.TA0010)

All three Collection/Exfiltration threats map to AML.T0009 (Collection).

- **T-EXFIL-001 Data Theft via web_fetch** — attacker exfiltrates data by instructing the agent to send it to an external URL, via prompt injection causing the agent to POST data to an attacker server; affects the `web_fetch` tool. Current mitigations: SSRF blocking for internal networks. Residual risk **High** (external URLs permitted). Recommends URL allowlisting and data-classification awareness.
- **T-EXFIL-002 Unauthorized Message Sending** — attacker causes the agent to send messages containing sensitive data, via prompt injection causing the agent to message the attacker; affects the message tool and channel integrations. Current mitigations: outbound messaging gating. Residual risk **Medium** (gating may be bypassed). Recommends explicit confirmation for new recipients.
- **T-EXFIL-003 Credential Harvesting** — a malicious skill harvests credentials from agent context by reading environment variables and config files; affects the skill execution environment. Current mitigations: **None specific to skills**. Residual risk **Critical** (skills run with agent privileges). Recommends skill sandboxing and credential isolation.

### 3.8 Impact (AML.TA0011)

All three Impact threats map to AML.T0031 (Erode AI Model Integrity).

- **T-IMPACT-001 Unauthorized Command Execution** — attacker executes arbitrary commands on the user system via prompt injection combined with exec-approval bypass; affects the Bash tool and command execution. Current mitigations: exec approvals, Docker sandbox option. Residual risk **Critical** (host execution without sandbox). Recommends defaulting to sandbox and improving approval UX.
- **T-IMPACT-002 Resource Exhaustion (DoS)** — attacker exhausts API credits or compute resources via automated message flooding and expensive tool calls; affects the Gateway, agent sessions, and API provider. Current mitigations: **None**. Residual risk **High** (no rate limiting). Recommends per-sender rate limits and cost budgets.
- **T-IMPACT-003 Reputation Damage** — attacker causes the agent to send harmful/offensive content via prompt injection causing inappropriate responses; affects output generation and channel messaging. Current mitigations: LLM-provider content policies. Residual risk **Medium** (provider filters imperfect). Recommends an output-filtering layer and user controls.

## §7.1 ATLAS Technique Mapping

The catalog rolls up to nine ATLAS technique IDs; each technique backs one or more `T-*` threats (the inverse index of the per-tactic catalog above):

| ATLAS ID | Technique Name | OpenClaw Threats |
| --- | --- | --- |
| AML.T0006 | Active Scanning | T-RECON-001, T-RECON-002 |
| AML.T0009 | Collection | T-EXFIL-001, T-EXFIL-002, T-EXFIL-003 |
| AML.T0010.001 | Supply Chain: AI Software | T-PERSIST-001, T-PERSIST-002 |
| AML.T0010.002 | Supply Chain: Data | T-PERSIST-003 |
| AML.T0031 | Erode AI Model Integrity | T-IMPACT-001, T-IMPACT-002, T-IMPACT-003 |
| AML.T0040 | AI Model Inference API Access | T-ACCESS-001, T-ACCESS-002, T-ACCESS-003, T-DISC-001, T-DISC-002 |
| AML.T0043 | Craft Adversarial Data | T-EXEC-004, T-EVADE-001, T-EVADE-002 |
| AML.T0051.000 | LLM Prompt Injection: Direct | T-EXEC-001, T-EXEC-003 |
| AML.T0051.001 | LLM Prompt Injection: Indirect | T-EXEC-002 |

## §7.3 Glossary

The source glossary defines the vocabulary the catalog uses: **ATLAS** — MITRE's Adversarial Threat Landscape for AI Systems; **ClawHub** — OpenClaw's skill marketplace; **Gateway** — OpenClaw's message routing and authentication layer; **MCP** — Model Context Protocol, the tool-provider interface; **Prompt Injection** — an attack where malicious instructions are embedded in input; **Skill** — a downloadable extension for OpenClaw agents; **SSRF** — Server-Side Request Forgery.

**Source**: OpenClaw documentation — `security/THREAT-MODEL-ATLAS` §3 / §7.1 / §7.3 (mirror `inbox/openclaw_docs/security/THREAT-MODEL-ATLAS.md`)
**Last Updated**: 2026-06-22
**Status**: Active
