---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - moderation
keywords:
  - clawhub moderation
  - clawhub reports
  - moderation holds
  - hidden or blocked listings
  - clawhub bans account standing
  - token revocation publishing access
  - clawhub appeal form
  - scan download fix reupload
  - publisher guidance false positives
topics:
  - OpenClaw
  - ClawHub Moderation
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/clawhub/moderation
access_control_group: ["general"]
---

# OpenClaw — ClawHub Moderation and Account Safety

## Overview

This note states ClawHub's moderation and account-safety **policy**: the argument for why an open publishing registry still needs guardrails, and the rules that govern reports, moderation holds, hidden/blocked listings, bans, account standing, and publisher conduct. It mirrors the `clawhub/moderation` source page. The framing claim is that ClawHub is "open to publishing, but public discovery and install surfaces still need guardrails" — so reports, moderation holds, hidden listings, and account actions exist to "protect users when a release or account appears unsafe, misleading, or out of policy." This page covers moderation and account standing only; the audit *labels* (`Pass`, `Review`, `Warn`, `Malicious`) and risk level are a distinct concept documented in Security Audits, and copyright/content-rights concerns route to Content Rights Requests rather than the report flow.

## Reports — what they are and are not for

Signed-in users can report skills, plugins, and packages. The policy scopes reports narrowly: ClawHub reports are **only for unsafe marketplace content**, namely malicious listings, misleading metadata, undeclared credentials or permission requirements, suspicious install instructions, impersonation, bad-faith registrations or trademark misuse, and content that violates Acceptable usage. Reports are filed via the **Report skill** button on a skill page, or via the package reporting command/API for packages.

The argument draws two firm boundaries on what reports must **not** be used for. First, reports are not for vulnerabilities in a third-party skill or plugin's **own source code** — those go directly to the publisher or the source repository linked from the listing, because "ClawHub does not maintain or patch third-party skill or plugin code." Second, GitHub Security Advisories for `openclaw/clawhub` are reserved for vulnerabilities in **ClawHub itself** (bugs in the website, API, CLI, registry, auth, scanning, moderation, or download/install trust boundaries) — and must not be used for third-party skill/plugin vulnerabilities. The page closes the section with a conduct rule: "Good reports are specific and actionable. Abuse of reporting can itself lead to account action" — i.e., the reporting channel is itself policed.

## Org and namespace claims (routing pointer)

Ownership disputes are deliberately routed **away** from both the in-product report flow and the account appeal form. Org, brand, package-scope, owner-handle, or namespace ownership disputes should instead use the Org and Namespace Claims process. That process is the right path "when you need ClawHub staff to review non-sensitive proof that a namespace should be reserved, transferred, renamed, hidden, quarantined, aliased, or otherwise reviewed." A hard data-handling rule applies to the public claim issue: do **not** include secrets, private documents, private legal files, personal identity documents, API tokens, or DNS challenge tokens. (Full filing procedure is in the namespace-claims note linked below.)

## Moderation holds

Severe findings or policy issues can place a publisher or listing under a **moderation hold**. When a hold is applied, affected content "may be hidden from public discovery, or future publishes may start hidden until the issue is reviewed." The stated justification is protective and time-bounded: moderation holds "are meant to protect users while ClawHub resolves high-risk cases," and — importantly for fairness — "they can also be lifted when a false positive is confirmed." A hold is therefore a reversible, risk-mitigating state, not a permanent sanction.

## Hidden or blocked listings

A listing may be in one of several unavailable states on public install surfaces: **held, hidden, quarantined, revoked, or otherwise unavailable**. The user-facing rule is a strong caution: "If you see one of these states, do not install the release unless the owner resolves the issue or moderation restores it." The policy preserves owner transparency despite the public block — owners "may still see diagnostics for their own held or hidden listings," and those diagnostics "help explain what happened and what needs to change before the listing can return to public surfaces." This separates the *public install gate* (closed) from the *owner remediation path* (open).

## Bans and account standing

Accounts that violate ClawHub policy "may lose publishing access," and severe abuse "can result in account bans, token revocation, hidden content, or removed listings." The downstream effect on automation is explicit: deleted, banned, or disabled accounts **cannot use ClawHub API tokens**, so CLI auth that starts failing after an account action is a symptom of changed account standing. The prescribed recovery sequence is: if CLI auth starts failing after account action, sign in to the web UI to review account state; and if sign-in or normal CLI access is blocked by a ban or disabled account, use the ClawHub appeal form (`https://appeals.openclaw.ai/`) for recovery review.

A distinct, self-service remediation path exists for scanner-triggered enforcement. If a scanner-triggered email names a skill or plugin version as malicious, the publisher should download the stored scan results for the blocked submitted version, review them, fix the listing, increment the version number, and upload the fixed version:

```bash
clawhub scan download <slug> --version <version>
```

For plugins, add `--kind plugin`. The policy thus distinguishes *appeal* (for account-level bans/disables, via the appeal form) from *fix-and-reupload* (for a specific malicious-flagged version, via `clawhub scan download` then a version bump).

## Publisher guidance

To reduce false positives and improve user trust, the page closes with publisher conduct guidance — the proactive complement to the enforcement rules above. Publishers should: keep names, summaries, tags, and changelogs accurate; declare required environment variables and permissions; avoid obfuscated install commands; link to source when possible; use dry runs before publishing plugins; and respond clearly if users or moderators ask about release behavior. These are the behaviors that keep a listing out of moderation holds and hidden/blocked states in the first place.

**Source**: OpenClaw documentation — `clawhub/moderation` (mirror `inbox/openclaw_docs/clawhub/moderation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
