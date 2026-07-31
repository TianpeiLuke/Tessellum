---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - incident_response
keywords:
  - openclaw incident response
  - security incident runbook
  - detection and triage
  - severity guide critical high medium low
  - coordinated disclosure cve ghsa
  - post-incident review follow-up
  - trust boundary impact triage
topics:
  - OpenClaw
  - Security Incident Response
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/security/incident-response
access_control_group: ["general"]
---

# OpenClaw — Security Incident Response Runbook

## Overview

This note is the OpenClaw security **incident-response runbook**: the five-step procedure for triaging, assessing, responding to, communicating, and following up on a security report or suspected incident. It mirrors the `security/incident-response` source page and is meant to be read when responding to a security report, preparing a coordinated disclosure or patched security release, or reviewing post-incident follow-up expectations. The runbook is the *live-vulnerability* path — distinct from threat-model contribution PRs, which go through the contribution guide instead. The five phases below — Detection and triage, Assessment, Response, Communication, Recovery and follow-up — are followed in order.

## 1. Detection and triage

OpenClaw monitors security signals from three sources:

- GitHub Security Advisories (GHSA) and private vulnerability reports.
- Public GitHub issues/discussions when reports are not sensitive.
- Automated signals (for example Dependabot, CodeQL, npm advisories, and secret scanning).

Initial triage runs three steps:

1. Confirm affected component, version, and trust boundary impact.
2. Classify as security issue vs hardening/no-action using the repository `SECURITY.md` scope and out-of-scope rules.
3. An incident owner responds accordingly.

## 2. Assessment

A reported issue is graded against a four-level severity guide that keys off trust-boundary impact, exploitation prerequisites, and the kind of control or data exposed:

- **Critical:** Package/release/repository compromise, active exploitation, or unauthenticated trust-boundary bypass with high-impact control or data exposure.
- **High:** Verified trust-boundary bypass requiring limited preconditions (for example authenticated but unauthorized high-impact action), or exposure of OpenClaw-owned sensitive credentials.
- **Medium:** Significant security weakness with practical impact but constrained exploitability or substantial prerequisites.
- **Low:** Defense-in-depth findings, narrowly scoped denial-of-service, or hardening/parity gaps without a demonstrated trust-boundary bypass.

## 3. Response

The response phase acknowledges, reproduces, patches, and ships, with the urgency set by the assessed severity:

1. Acknowledge receipt to the reporter (private when sensitive).
2. Reproduce on supported releases and latest `main`, then implement and validate a patch with regression coverage.
3. For critical/high incidents, prepare patched release(s) as fast as practical.
4. For medium/low incidents, patch in normal release flow and document mitigation guidance.

## 4. Communication

OpenClaw communicates incident status and fixes through three channels:

- GitHub Security Advisories in the affected repository.
- Release notes/changelog entries for fixed versions.
- Direct reporter follow-up on status and resolution.

The disclosure policy is severity-dependent:

- Critical/high incidents should receive coordinated disclosure, with CVE issuance when appropriate.
- Low-risk hardening findings may be documented in release notes or advisories without CVE, depending on impact and user exposure.

## 5. Recovery and follow-up

After shipping the fix, three recovery steps close out the incident and harden against recurrence:

1. Verify remediations in CI and release artifacts.
2. Run a short post-incident review (timeline, root cause, detection gap, prevention plan).
3. Add follow-up hardening/tests/docs tasks and track them to completion.

**Source**: OpenClaw documentation — `security/incident-response` (mirror `inbox/openclaw_docs/security/incident-response.md`)
**Last Updated**: 2026-06-22
**Status**: Active
