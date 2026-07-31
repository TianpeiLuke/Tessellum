---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - threat_model
keywords:
  - openclaw threat model contribution
  - contribute a threat
  - threat id categories
  - atlas mapping submission
  - risk levels critical high medium low
  - threat model review process
  - attack chain proposal
  - live vulnerability vs threat model
topics:
  - OpenClaw
  - Security Threat Model
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/security/CONTRIBUTING-THREAT-MODEL
access_control_group: ["general"]
---

# OpenClaw — Contributing to the Threat Model

## Overview

This note is the **procedure for contributing to the OpenClaw threat model** — the living, MITRE-ATLAS-framed catalog of attack vectors against OpenClaw. It mirrors the `security/CONTRIBUTING-THREAT-MODEL` source page: the four ways to contribute (add a threat, suggest a mitigation, propose an attack chain, fix existing content), the taxonomy maintainers use (the MITRE ATLAS framework, the threat-ID category codes, and the four risk levels), the four-step maintainer review process, plus the resources, contact channels, and recognition for contributors. The page stresses one hard boundary: this process is for **adding to the threat model, not reporting live vulnerabilities** — exploitable bugs go through responsible disclosure instead. Contributors do not need to be security experts: describe a scenario in your own words and maintainers handle the ATLAS mapping, threat IDs, and risk assessment during review.

## Ways to Contribute

The threat model accepts four kinds of contribution. None requires framework knowledge.

### Add a threat

Spotted an attack vector or risk not yet covered? Open an issue on `openclaw/trust` (`https://github.com/openclaw/trust/issues`) and describe it in your own words — no need to know any frameworks or fill in every field, just describe the scenario. **Helpful to include (but not required):**

- The attack scenario and how it could be exploited.
- Which parts of OpenClaw are affected (CLI, gateway, channels, ClawHub, MCP servers, etc.).
- How severe you think it is (low / medium / high / critical).
- Any links to related research, CVEs, or real-world examples.

Maintainers handle the ATLAS mapping, threat IDs, and risk assessment during review; including those details is welcome but not expected.

### Suggest a mitigation

Have an idea for how to address an existing threat? Open an issue or PR **referencing the threat**. Useful mitigations are *specific and actionable* — the source contrasts `"per-sender rate limiting of 10 messages/minute at the gateway"` (good) against `"implement rate limiting"` (too vague).

### Propose an attack chain

Attack chains show how multiple threats combine into a realistic attack scenario. If you see a dangerous combination, describe the steps and how an attacker would chain them together. Per source, *a short narrative of how the attack unfolds in practice is more valuable than a formal template.*

### Fix or improve existing content

Typos, clarifications, outdated info, and better examples are welcome as **PRs — no issue needed**.

## Live Vulnerabilities Are Out of Scope (Hard Boundary)

The source calls this out as a blockquote: **this process is for adding to the threat model, not reporting live vulnerabilities.** If you have found an exploitable vulnerability, the contribution path does NOT apply — instead, see the OpenClaw [Trust page](https://trust.openclaw.ai) for responsible-disclosure instructions. Threat-model contributions describe *potential* attack vectors and mitigations as a living-document update; live-vuln reports are handled through coordinated disclosure and tracked through the incident-response runbook.

## What Maintainers Use (Taxonomy)

Three things frame every accepted contribution. Contributors are *not* required to apply them — maintainers assign them during review.

### MITRE ATLAS framework

The threat model is built on **MITRE ATLAS** ([atlas.mitre.org](https://atlas.mitre.org/)) — *Adversarial Threat Landscape for AI Systems* — a framework designed specifically for AI/ML threats like **prompt injection, tool misuse, and agent exploitation**. Per source: *you don't need to know ATLAS to contribute — we map submissions to the framework during review.*

### Threat IDs

Each threat gets an ID like `T-EXEC-003`. The category codes (assigned by maintainers during review — contributors do not need to pick one) are:

| Code    | Category                                   |
| ------- | ------------------------------------------ |
| RECON   | Reconnaissance - information gathering     |
| ACCESS  | Initial access - gaining entry             |
| EXEC    | Execution - running malicious actions      |
| PERSIST | Persistence - maintaining access           |
| EVADE   | Defense evasion - avoiding detection       |
| DISC    | Discovery - learning about the environment |
| EXFIL   | Exfiltration - stealing data               |
| IMPACT  | Impact - damage or disruption              |

### Risk levels

Submissions are graded on four levels (if unsure, describe the impact and maintainers assess it):

| Level        | Meaning                                                           |
| ------------ | ----------------------------------------------------------------- |
| **Critical** | Full system compromise, or high likelihood + critical impact      |
| **High**     | Significant damage likely, or medium likelihood + critical impact |
| **Medium**   | Moderate risk, or low likelihood + high impact                    |
| **Low**      | Unlikely and limited impact                                       |

## Review Process

Maintainers run accepted submissions through four steps (verbatim from source):

1. **Triage** — new submissions are reviewed within **48 hours**.
2. **Assessment** — maintainers verify feasibility, assign the ATLAS mapping and threat ID, and validate the risk level.
3. **Documentation** — they ensure everything is formatted and complete.
4. **Merge** — the threat is added to the threat model and visualization.

## Resources, Contact, and Recognition

**Resources** the source links for contributors: the [ATLAS Website](https://atlas.mitre.org/), [ATLAS Techniques](https://atlas.mitre.org/techniques/), [ATLAS Case Studies](https://atlas.mitre.org/studies/), and the [OpenClaw Threat Model](https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS) itself.

**Contact** — three channels, scoped by purpose: security vulnerabilities go to the [Trust page](https://trust.openclaw.ai) for reporting instructions (NOT the issue tracker); threat-model questions go to an issue on `openclaw/trust` (`https://github.com/openclaw/trust/issues`); general chat is the Discord `#security` channel.

**Recognition** — contributors to the threat model are recognized in the threat-model acknowledgments, in release notes, and (for significant contributions) in the **OpenClaw security hall of fame**.

**Source**: OpenClaw documentation — `security/CONTRIBUTING-THREAT-MODEL` (mirror `inbox/openclaw_docs/security/CONTRIBUTING-THREAT-MODEL.md`)
**Last Updated**: 2026-06-22
**Status**: Active
