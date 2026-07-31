---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - security
keywords:
  - clawhub security audit result
  - audit status pass review warn malicious
  - risk level low medium high
  - findings info critical severity
  - pre-install trust checklist
  - blast radius authority
  - install decision skill plugin
topics:
  - OpenClaw
  - ClawHub Security Audits
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/clawhub/security-audits
access_control_group: ["general"]
---

# OpenClaw — ClawHub Security Audit Result Schema (Status, Risk, Findings)

## Overview

This note models the **install-time security-audit result** a user reads on ClawHub before installing a skill or plugin, mirroring the result-schema half of the `clawhub/security-audits` source page (the intro, "What to check before installing", "Audit status", "Risk level", and "Findings" sections). It is the user-facing projection of ClawHub's per-release security review: three coordinated dimensions — an **audit status** (what to do with the result), a **risk level** (how much power the release has), and a list of **findings** (the severity-graded evidence behind both) — plus a pre-install trust checklist. The companion note [oc_clawhub_security_audits_scan_stack](oc_clawhub_security_audits_scan_stack.md) covers how that result is produced (SkillSpector + VirusTotal + ClawScan); this note covers only the result schema and the install decision it supports.

A ClawHub audit is a **strong safety signal but not a guarantee** that a release is risk-free — the source states explicitly that you should "always use judgment before granting sensitive access." The audit shows what a release does, what authority it asks for, and whether anything deserves extra attention before it can access files, accounts, credentials, code, or external services.

## What to Check Before Installing

The source page gives an explicit pre-install review list. Before installing, review:

- the overall audit status
- the risk level
- any listed findings
- required credentials, permissions, or environment variables
- owner, source, version, changelog, installs, stars, and other trust signals

The page closes the checklist with a single decision rule: **"Install only content you understand and trust."** Notice that the audit status, risk level, and findings are only the first three rows — the remaining rows (required credentials/permissions/env vars, and the owner/source/version/changelog/installs/stars trust signals) are signals the audit does *not* fully decide for you and that you weigh yourself.

## Audit Status

**Audit status tells you how to react to the audit result** — it answers the question "What should I do with this result?" There are six statuses, reproduced verbatim from the source page:

| Status      | Meaning                                                                   |
| ----------- | ------------------------------------------------------------------------- |
| `Pass`      | No visible issue above low risk was found.                                |
| `Review`    | Read the findings before installing. The release may still be legitimate. |
| `Warn`      | Use extra caution. ClawHub found a high-impact concern or warning signal. |
| `Malicious` | Do not install.                                                           |
| `Pending`   | Audits have not finished yet.                                             |
| `Error`     | The audit could not be completed.                                         |

A `Pass` is reassuring, but **it does not replace your own judgment**. The source emphasizes this matters most for tools that can publish content, edit data, run commands, read files, or access production systems. `Pending` and `Error` are not safety verdicts at all — they mean the audit has not finished (`Pending`) or could not be completed (`Error`), so there is no result to rely on yet.

## Risk Level

**Risk level describes blast radius: how much power the release appears to have if you use it as intended.** It answers a different question from audit status — "How much power is here?" There are three levels, reproduced verbatim:

| Risk level | Meaning                                                                       |
| ---------- | ----------------------------------------------------------------------------- |
| `Low`      | Little sensitive authority or user impact was found.                          |
| `Medium`   | The release has meaningful authority, such as account access or data changes. |
| `High`     | The release has high-impact authority, severe findings, or malicious signals. |

## Status vs Risk: Two Independent Questions

The source draws the two axes apart explicitly — they answer different questions and must not be conflated:

- **Risk level asks:** "How much power is here?"
- **Audit status asks:** "What should I do with this result?"

The worked example from the page: a publishing skill may show **`Review` with `Medium` risk**. Per the source, that does *not* mean it is malicious — it means the skill appears purpose-aligned, but can act with meaningful account authority. In other words, a release can legitimately carry `Medium` (or higher) authority and still be safe to install once you have read the findings; the `Review` status is a prompt to look, not a denial.

## Findings

**Findings explain why an audit result was shown** — they are the evidence rolled up into the status and risk level above. Each finding usually includes:

- what it means
- why it was flagged
- the relevant skill or plugin content
- a recommendation

Findings are graded by severity. They may be labeled **`Info`, `Low`, `Medium`, `High`, or `Critical`** (in ascending order). Per the source, **higher-severity findings contribute more strongly to risk level and audit status** — i.e., severity is the per-finding signal that aggregates upward into the two summary dimensions. Finally, **low-confidence findings are hidden from the public audit rollup** so the page stays focused on useful evidence (they are suppressed from the visible summary, not necessarily absent from the underlying analysis).

**Source**: OpenClaw documentation — `clawhub/security-audits` (mirror `inbox/openclaw_docs/clawhub/security-audits.md`)
**Last Updated**: 2026-06-22
**Status**: Active
