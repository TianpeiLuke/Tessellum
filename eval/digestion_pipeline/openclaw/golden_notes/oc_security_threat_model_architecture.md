---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - threat_model
keywords:
  - openclaw threat model
  - mitre atlas threat model
  - openclaw trust boundaries
  - channel access session isolation
  - tool execution sandbox boundary
  - external content supply chain boundary
  - data flow protections F1 F6
  - in-scope component matrix
topics:
  - OpenClaw
  - Security Architecture
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS
access_control_group: ["general"]
---

# OpenClaw — Threat Model: Architecture and Trust Boundaries

## Overview

This note models the **architecture layer** of OpenClaw's MITRE-ATLAS threat model: the framework it is built on, the in-scope component matrix, the five concentric trust boundaries an inbound message crosses (Channel Access → Session Isolation → Tool Execution → External Content → Supply Chain), and the six labelled data flows (F1–F6) with their protections. It mirrors the `security/THREAT-MODEL-ATLAS` source page sections "MITRE ATLAS framework", "Contributing to This Threat Model", "§1 Introduction" (Purpose / Scope / Out of Scope), and "§2 System Architecture" (2.1 Trust Boundaries, 2.2 Data Flows). The per-ATLAS-tactic threat catalog (§3, §7), the ClawHub supply-chain deep-dive (§4–6), and the contribution process are sibling notes; this note is the structural reference they point back to.

## MITRE ATLAS Framework

The threat model is **version 1.0-draft** (Last Updated 2026-02-04) and uses a **MITRE ATLAS + Data Flow Diagrams** methodology. It is built on [MITRE ATLAS](https://atlas.mitre.org/) — the Adversarial Threat Landscape for AI Systems, the industry-standard framework for documenting adversarial threats to AI/ML systems, maintained by MITRE in collaboration with the AI security community. The page lists these key ATLAS resources: ATLAS Techniques, ATLAS Tactics, ATLAS Case Studies, the ATLAS GitHub (`mitre-atlas/atlas-data`), and Contributing to ATLAS. Because the framing is ATLAS, every threat catalogued elsewhere in the model carries an `AML.T0xxx` ATLAS technique ID.

The threat model is a **living document maintained by the OpenClaw community**; the source points contributors to `CONTRIBUTING-THREAT-MODEL.md` (note 4) for guidelines on reporting new threats, updating existing threats, proposing attack chains, and suggesting mitigations.

## §1 Introduction

**1.1 Purpose** — The threat model documents adversarial threats to the OpenClaw AI agent platform and the ClawHub skill marketplace, using the MITRE ATLAS framework designed specifically for AI/ML systems.

**1.2 Scope** — The in-scope component matrix marks the runtime, gateway, channels, marketplace, and tool providers as included, with user devices only partially in scope:

| Component | Included | Notes |
| --- | --- | --- |
| OpenClaw Agent Runtime | Yes | Core agent execution, tool calls, sessions |
| Gateway | Yes | Authentication, routing, channel integration |
| Channel Integrations | Yes | WhatsApp, Telegram, Discord, Signal, Slack, etc. |
| ClawHub Marketplace | Yes | Skill publishing, moderation, distribution |
| MCP Servers | Yes | External tool providers |
| User Devices | Partial | Mobile apps, desktop clients |

**1.3 Out of Scope** — "Nothing is explicitly out of scope for this threat model." (verbatim) — i.e., the model intentionally claims complete component coverage rather than carving out exclusions.

## §2 System Architecture

### 2.1 Trust Boundaries

An inbound message originates in the **UNTRUSTED ZONE** (the messaging channels — WhatsApp, Telegram, Discord, and others) and flows downward through five concentric trust boundaries. Each boundary is a control surface where the message is authenticated, isolated, gated, sanitized, or screened before it can affect the next layer. The source renders this as an ASCII trust-boundary diagram reproduced verbatim below:

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNTRUSTED ZONE                                │
│  WhatsApp · Telegram · Discord · ...                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
   TRUST BOUNDARY 1: Channel Access — GATEWAY
   • Device Pairing (1h DM / 5m node grace period)
   • AllowFrom / AllowList validation
   • Token/Password/Tailscale auth
                              │
                              ▼
   TRUST BOUNDARY 2: Session Isolation — AGENT SESSIONS
   • Session key = agent:channel:peer
   • Tool policies per agent
   • Transcript logging
                              │
                              ▼
   TRUST BOUNDARY 3: Tool Execution — EXECUTION SANDBOX
   • Docker sandbox OR Host (exec-approvals)
   • Node remote execution
   • SSRF protection (DNS pinning + IP blocking)
                              │
                              ▼
   TRUST BOUNDARY 4: External Content — FETCHED URLs / EMAILS / WEBHOOKS
   • External content wrapping (XML tags)
   • Security notice injection
                              │
                              ▼
   TRUST BOUNDARY 5: Supply Chain — CLAWHUB
   • Skill publishing (semver, SKILL.md required)
   • Pattern-based moderation flags
   • VirusTotal scanning (coming soon)
   • GitHub account age verification
```

**Trust Boundary 1 — Channel Access (Gateway).** The gateway is the first control surface: it does device pairing (a 1-hour grace period for DM channel pairing, 5 minutes for node pairing), `AllowFrom` / `AllowList` validation, and Token/Password/Tailscale authentication. Messages from the untrusted zone cannot reach a session without crossing this boundary.

**Trust Boundary 2 — Session Isolation (Agent Sessions).** Past the gateway, each conversation is isolated by a **session key of the form `agent:channel:peer`**, with per-agent tool policies and transcript logging. The session key is the isolation primitive that prevents one peer's context from leaking into another's.

**Trust Boundary 3 — Tool Execution (Execution Sandbox).** Tool/command execution happens either in a **Docker sandbox OR on the Host (gated by exec-approvals)**, supports node remote execution, and enforces **SSRF protection via DNS pinning + IP blocking**. This boundary contains the blast radius of any tool the agent is induced to call.

**Trust Boundary 4 — External Content (Fetched URLs / Emails / Webhooks).** Content the agent fetches (URLs, emails, webhooks) is treated as untrusted: it is wrapped in XML tags ("external content wrapping") with security-notice injection so the model can distinguish operator instructions from fetched data. This boundary is the structural defense against indirect prompt injection.

**Trust Boundary 5 — Supply Chain (ClawHub).** Skills distributed through ClawHub cross a supply-chain boundary: skill publishing requires semver + a `SKILL.md`, pattern-based moderation flags screen submissions, VirusTotal scanning is "coming soon", and GitHub account age verification raises the bar for new attacker accounts. The deep-dive on this boundary is note 3.

### 2.2 Data Flows

The architecture defines six labelled data flows, each with a source, destination, the data carried, and the protection applied at that hop:

| Flow | Source | Destination | Data | Protection |
| --- | --- | --- | --- | --- |
| F1 | Channel | Gateway | User messages | TLS, AllowFrom |
| F2 | Gateway | Agent | Routed messages | Session isolation |
| F3 | Agent | Tools | Tool invocations | Policy enforcement |
| F4 | Agent | External | web_fetch requests | SSRF blocking |
| F5 | ClawHub | Agent | Skill code | Moderation, scanning |
| F6 | Agent | Channel | Responses | Output filtering |

The data-flow protections map onto the trust boundaries: **F1** (channel→gateway, TLS + AllowFrom) is Boundary 1; **F2** (gateway→agent, session isolation) is Boundary 2; **F3** (agent→tools, policy enforcement) and **F4** (agent→external, SSRF blocking) realize Boundary 3 and the egress side of Boundary 4; **F5** (ClawHub→agent skill code, moderation + scanning) is Boundary 5; and **F6** (agent→channel responses, output filtering) is the outbound return path. F4's SSRF-blocking protection is the operator-tunable egress surface the network-proxy notes (7/8) extend.

**Source**: OpenClaw documentation — `security/THREAT-MODEL-ATLAS` (mirror `inbox/openclaw_docs/security/THREAT-MODEL-ATLAS.md`)
**Last Updated**: 2026-06-22
**Status**: Active
