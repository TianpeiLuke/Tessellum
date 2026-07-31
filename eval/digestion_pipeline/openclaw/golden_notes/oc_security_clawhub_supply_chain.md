---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - supply_chain
keywords:
  - clawhub supply chain
  - moderation flag rules
  - skill marketplace security
  - virustotal code insight
  - risk matrix likelihood impact
  - critical path attack chains
  - p0 p1 p2 recommendations
  - key security files
topics:
  - OpenClaw
  - Security
  - Supply Chain
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS
access_control_group: ["general"]
---

# OpenClaw — ClawHub Supply-Chain Security, Risk Matrix, and Recommendations

## Overview

This note argues the supply-chain security posture of **ClawHub**, OpenClaw's skill marketplace (Trust Boundary 5), drawing from §4–6 plus §7.2 of the `security/THREAT-MODEL-ATLAS` source page. It catalogs the current ClawHub controls and their candid effectiveness ratings, reproduces the `moderation.ts` FLAG_RULES regex patterns and their stated limits, lists the planned improvements (VirusTotal Code Insight, community reporting, audit logging, badges), then presents the quantified likelihood×impact risk matrix, the three critical-path attack chains, and the P0–P2 recommendation roadmap, closing with the Key Security Files index. The throughline argument: ClawHub's present controls are **shallow (slug/metadata-only, regex-based, no code analysis, no sandboxing)**, so supply-chain threats remain among the highest residual risks until behavioral analysis and skill sandboxing land.

## 4. ClawHub Supply Chain Analysis

### 4.1 Current Security Controls

ClawHub applies seven controls at publish/distribution time. The source rates each control's effectiveness candidly — most are Medium-to-Low, which is the core of the supply-chain argument: the bar is raised for casual attackers but not for determined ones.

| Control | Implementation | Effectiveness |
| --- | --- | --- |
| GitHub Account Age | `requireGitHubAccountAge()` | Medium — Raises bar for new attackers |
| Path Sanitization | `sanitizePath()` | High — Prevents path traversal |
| File Type Validation | `isTextFile()` | Medium — Only text files, but can still be malicious |
| Size Limits | 50MB total bundle | High — Prevents resource exhaustion |
| Required SKILL.md | Mandatory readme | Low security value — Informational only |
| Pattern Moderation | FLAG_RULES in moderation.ts | Low — Easily bypassed |
| Moderation Status | `moderationStatus` field | Medium — Manual review possible |

The two High-rated controls (`sanitizePath()` path-traversal prevention, the 50MB bundle size limit) defend against mechanical/resource abuse rather than malicious *content* — the content-trust controls (`requireGitHubAccountAge()`, `isTextFile()`, FLAG_RULES pattern moderation, the `moderationStatus` manual-review field) are all rated Medium or Low, and the mandatory `SKILL.md` readme is explicitly "Low security value — Informational only."

### 4.2 Moderation Flag Patterns

The pattern-based moderation in `moderation.ts` applies these FLAG_RULES (reproduced verbatim from source):

```javascript
// Known-bad identifiers
/(keepcold131\/ClawdAuthenticatorTool|ClawdAuthenticatorTool)/i

// Suspicious keywords
/(malware|stealer|phish|phishing|keylogger)/i
/(api[-_ ]?key|token|password|private key|secret)/i
/(wallet|seed phrase|mnemonic|crypto)/i
/(discord\.gg|webhook|hooks\.slack)/i
/(curl[^\n]+\|\s*(sh|bash))/i
/(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd)/i
```

The source enumerates four explicit **limitations** that drive the "Low — Easily bypassed" effectiveness rating: the rules only check `slug`, `displayName`, `summary`, frontmatter, metadata, and file paths; they do **not** analyze the actual skill code content; the simple regex is easily bypassed with obfuscation; and there is no behavioral analysis. This is the textual evidence that ties §4.2 to threat T-EVADE-001 (Moderation Pattern Bypass via Unicode homoglyphs / encoding tricks / dynamic loading) catalogued in the companion threat-catalog note.

### 4.3 Planned Improvements

Four improvements are tracked, each with a status and expected impact:

| Improvement | Status | Impact |
| --- | --- | --- |
| VirusTotal Integration | In Progress | High — Code Insight behavioral analysis |
| Community Reporting | Partial (`skillReports` table exists) | Medium |
| Audit Logging | Partial (`auditLogs` table exists) | Medium |
| Badge System | Implemented | Medium — `highlighted`, `official`, `deprecated`, `redactionApproved` |

The headline planned control is **VirusTotal Integration** (In Progress) delivering Code Insight behavioral analysis — the source's named answer to the §4.2 "no behavioral analysis" gap. Community Reporting and Audit Logging are both Partial (the `skillReports` and `auditLogs` tables already exist) and the Badge System is Implemented, exposing the `highlighted`, `official`, `deprecated`, and `redactionApproved` badge values.

## 5. Risk Matrix

### 5.1 Likelihood vs Impact

The risk matrix scores each catalogued threat on Likelihood × Impact → Risk Level → Priority. Of the 13 ranked threats, the three **Critical / P0** entries are dominated by the supply-chain and execution surfaces this note centers on (malicious skill install, credential harvesting), reinforcing the argument that ClawHub supply chain is OpenClaw's top-tier residual risk.

| Threat ID | Likelihood | Impact | Risk Level | Priority |
| --- | --- | --- | --- | --- |
| T-EXEC-001 | High | Critical | **Critical** | P0 |
| T-PERSIST-001 | High | Critical | **Critical** | P0 |
| T-EXFIL-003 | Medium | Critical | **Critical** | P0 |
| T-IMPACT-001 | Medium | Critical | **High** | P1 |
| T-EXEC-002 | High | High | **High** | P1 |
| T-EXEC-004 | Medium | High | **High** | P1 |
| T-ACCESS-003 | Medium | High | **High** | P1 |
| T-EXFIL-001 | Medium | High | **High** | P1 |
| T-IMPACT-002 | High | Medium | **High** | P1 |
| T-EVADE-001 | High | Medium | **Medium** | P2 |
| T-ACCESS-001 | Low | High | **Medium** | P2 |
| T-ACCESS-002 | Low | High | **Medium** | P2 |
| T-PERSIST-002 | Low | High | **Medium** | P2 |

T-PERSIST-001 (Malicious Skill Installation, High×Critical) and T-EXFIL-003 (Credential Harvesting, Medium×Critical) are both P0 supply-chain threats; T-PERSIST-002 (Skill Update Poisoning) is Low×High → Medium P2; T-EVADE-001 (Moderation Pattern Bypass) is High×Medium → Medium P2 — the moderation-bypass threat is *likely* but lower-impact than the skill-install threat it enables.

### 5.2 Critical Path Attack Chains

The source models three end-to-end attack chains; **Attack Chain 1** is the canonical ClawHub supply-chain kill chain (publish → evade → harvest), composed entirely of the threats this note's risk matrix ranks:

```
Attack Chain 1: Skill-Based Data Theft
T-PERSIST-001 → T-EVADE-001 → T-EXFIL-003
(Publish malicious skill) → (Evade moderation) → (Harvest credentials)

Attack Chain 2: Prompt Injection to RCE
T-EXEC-001 → T-EXEC-004 → T-IMPACT-001
(Inject prompt) → (Bypass exec approval) → (Execute commands)

Attack Chain 3: Indirect Injection via Fetched Content
T-EXEC-002 → T-EXFIL-001 → External exfiltration
(Poison URL content) → (Agent fetches & follows instructions) → (Data sent to attacker)
```

Chain 1 directly composes the §4 controls' weaknesses: a skill published past `requireGitHubAccountAge()` (T-PERSIST-001) evades the regex FLAG_RULES via obfuscation (T-EVADE-001), then harvests credentials because skills run with agent privileges and there is no skill sandboxing (T-EXFIL-003). Chains 2 and 3 are execution/exfiltration chains shared with the threat-catalog note but listed here because §5.2 is the consolidated attack-chain section.

## 6. Recommendations Summary

The recommendation roadmap is tiered P0 (Immediate) → P1 (Short-term) → P2 (Medium-term). The P0 tier is the supply-chain core of the argument: complete VirusTotal integration and implement skill sandboxing — the two controls that close the §4.2 "no behavioral analysis" and §4.1 "no sandboxing" gaps.

### 6.1 Immediate (P0)

| ID | Recommendation | Addresses |
| --- | --- | --- |
| R-001 | Complete VirusTotal integration | T-PERSIST-001, T-EVADE-001 |
| R-002 | Implement skill sandboxing | T-PERSIST-001, T-EXFIL-003 |
| R-003 | Add output validation for sensitive actions | T-EXEC-001, T-EXEC-002 |

### 6.2 Short-term (P1)

| ID | Recommendation | Addresses |
| --- | --- | --- |
| R-004 | Implement rate limiting | T-IMPACT-002 |
| R-005 | Add token encryption at rest | T-ACCESS-003 |
| R-006 | Improve exec approval UX and validation | T-EXEC-004 |
| R-007 | Implement URL allowlisting for web_fetch | T-EXFIL-001 |

### 6.3 Medium-term (P2)

| ID | Recommendation | Addresses |
| --- | --- | --- |
| R-008 | Add cryptographic channel verification where possible | T-ACCESS-002 |
| R-009 | Implement config integrity verification | T-PERSIST-003 |
| R-010 | Add update signing and version pinning | T-PERSIST-002 |

R-001 (VirusTotal) and R-002 (skill sandboxing) jointly address the two P0 supply-chain threats T-PERSIST-001 and T-EXFIL-003 and the P2 T-EVADE-001 — closing Attack Chain 1. R-010 (update signing + version pinning) is the medium-term answer to T-PERSIST-002 Skill Update Poisoning, where auto-updates may pull a compromised version.

## 7.2 Key Security Files

The threat model's appendix maps each critical mitigation to its source file and a risk level. These are the code-side counterparts that `repo_openclaw_security` documents (linked, not recreated here):

| Path | Purpose | Risk Level |
| --- | --- | --- |
| `src/infra/exec-approvals.ts` | Command approval logic | **Critical** |
| `src/gateway/auth.ts` | Gateway authentication | **Critical** |
| `src/infra/net/ssrf.ts` | SSRF protection | **Critical** |
| `src/security/external-content.ts` | Prompt injection mitigation | **Critical** |
| `src/agents/sandbox/tool-policy.ts` | Tool policy enforcement | **Critical** |
| `src/routing/resolve-route.ts` | Session isolation | **Medium** |

For the ClawHub moderation surface specifically, the source elsewhere names `moderation.ts` (FLAG_RULES, §4.2) as the marketplace control point; the skill-publishing pipeline, badge fields, and the `skillReports` / `auditLogs` tables are the §4.1/4.3 data-plane artifacts.

**Source**: OpenClaw documentation — `security/THREAT-MODEL-ATLAS` §4–6 + §7.2 (mirror `inbox/openclaw_docs/security/THREAT-MODEL-ATLAS.md`)
**Last Updated**: 2026-06-22
**Status**: Active
