---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - security
keywords:
  - clawhub security audit scan stack
  - clawscan skillspector virustotal
  - owasp agentic skills top 10
  - artifact-aware coherence check
  - declared metadata vs actual behavior
  - virustotal vendor count telemetry
  - prompt injection tool misuse excessive agency
  - security-audit page path
topics:
  - OpenClaw
  - ClawHub Security Audits
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/clawhub/security-audits
access_control_group: ["general"]
---

# OpenClaw — ClawHub Security-Audit Scan Stack

## Overview

This note explains the **concept of how ClawHub produces a security audit** for a skill or plugin release — the scanning pipeline behind the status / risk / findings a user reads before installing. It covers the three sections the `security-audits` source page assigns here: **What ClawHub checks** (which release artifacts are scanned, the central coherence question, and the per-artifact `security-audit` page path), **VirusTotal** (its role as malware telemetry and the plain-language vendor-count summaries), and **Risk analysis** (ClawScan as ClawHub's own agent-aware audit system, the static-scan-signal input, and the OWASP Agentic Skills Top 10 lens). The user-facing result schema this pipeline emits — audit status, risk level, and findings — is documented separately in the sibling result-schema note; this note is the producer side.

## What ClawHub Checks

ClawHub audits **submitted release artifacts**. Per the source, the audited material includes:

- skill instructions or plugin metadata
- declared environment variables and permissions
- install instructions and package metadata
- included files and file manifests
- compatibility and capability metadata

The central evaluation is **coherence**: the main question is "do the name, summary, metadata, requested authority, and actual content line up with what users would reasonably expect?" The audit is therefore not a blunt capability blocklist — the source is explicit that **powerful behavior is not automatically bad**. Many useful tools legitimately need credentials, local commands, provider APIs, or package installs; the audit instead checks whether that power is **expected, disclosed, and proportionate**. This makes the declared metadata (the skill's `metadata.openclaw` frontmatter and declared permissions) load-bearing input — a release whose declarations match its behavior reads as coherent, while a mismatch between declaration and actual content is what draws scrutiny.

Each artifact page links out to its full audit at a stable per-release path:

```text
/<owner>/<slug>/security-audit
```

That **audit page combines** three components, enumerated in source order:

1. SkillSpector
2. VirusTotal
3. Risk analysis

## VirusTotal

ClawHub uses **VirusTotal as malware telemetry in the audit stack**. The source frames VirusTotal as "a trusted industry standard for file reputation and malware scanning," and states ClawHub's partnership "lets ClawHub add broader security intelligence to skill and plugin review." It is described as especially useful for **known malicious artifacts, engine hits, and reputation signals** that complement ClawHub's own agent-aware review.

When vendor engine counts are available, the audit **summarizes them in plain language**. The source gives these example renderings verbatim:

```text
62/62 vendors flagged this skill as clean.
```

```text
2/64 vendors flagged this skill as malicious, 1/64 flagged it as suspicious, and 61/64 flagged it as clean.
```

When ClawHub has no vendor-count telemetry to summarize, the audit instead says `No VirusTotal findings`. Critically, the source draws a boundary on what VirusTotal contributes: **VirusTotal remains telemetry — "It does not replace ClawHub's own artifact-aware risk analysis."** It is one reputation/malware input, not the verdict.

## Risk Analysis (ClawScan)

**Risk analysis is powered internally by ClawScan, ClawHub's own security audit system.** ClawScan reviews each release as an **agent-facing artifact**, taking as input the full set of signals the source enumerates: instructions, metadata, declared permissions, files, capability signals, static scan signals, SkillSpector findings, VirusTotal telemetry, and publisher-provided context. The source clarifies the standing of one of these inputs: **static scan signals are internal context for this review; they are not a standalone public audit section or an install-blocking verdict.** In other words, static scanning feeds the agent-aware analysis rather than acting as its own gate.

### The OWASP Agentic Skills Top 10 Lens

Risk analysis uses the **[OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)** as a lens for risks. The source names the following risk classes evaluated through that lens (verbatim list): **prompt injection, tool misuse, credential exposure, unsafe execution, memory or context poisoning, and excessive agency.** These are applied as an evaluation frame over the agent-facing artifact — they are the threat categories ClawScan looks for, not separate scanners.

### Disclosed, Purpose-Aligned, Proportionate

Consistent with the "What ClawHub checks" coherence principle, **ClawScan does not treat a scary-looking capability as automatically malicious.** The source states it instead asks whether the capability is **disclosed, purpose-aligned, and supported by the release's stated use case.** This is the same disclosed-and-proportionate test applied at the analysis layer: a release that requests broad authority but openly declares it and uses it for its stated purpose can still read as acceptable, whereas undisclosed or mismatched power is what elevates concern. The output of this analysis — together with SkillSpector and VirusTotal — rolls up into the audit status, risk level, and findings consumed by the result-schema note.

**Source**: OpenClaw documentation — `clawhub/security-audits` (mirror `inbox/openclaw_docs/clawhub/security-audits.md`)
**Last Updated**: 2026-06-22
**Status**: Active
