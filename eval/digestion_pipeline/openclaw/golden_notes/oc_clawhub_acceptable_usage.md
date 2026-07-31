---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - acceptable_usage
keywords:
  - clawhub acceptable usage policy
  - disallowed marketplace behavior
  - ban evasion fake engagement
  - bulk low-effort publishing
  - pipe-to-shell unsafe execution
  - non-consensual impersonation
  - review and enforcement actions
  - content rights request copyright
topics:
  - OpenClaw
  - ClawHub Acceptable Usage
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/clawhub/acceptable-usage
access_control_group: ["general"]
---

# OpenClaw — ClawHub Acceptable Usage Policy

## Overview

This note states ClawHub's **acceptable-usage policy** — the argument for what the marketplace will and will not host, and why publishing behavior (not just listing content) is governed. ClawHub hosts skills, plugins, packages, and marketplace metadata for OpenClaw, and the policy applies to four things: what a listing *does*, what it *asks users to run*, how it *represents itself*, and how publishers use ClawHub's discovery, install, and trust surfaces. This note mirrors the `clawhub/acceptable-usage` source page in full — Allowed content, Disallowed content, Disallowed marketplace behavior, Content rights, and Review and enforcement — and folds the thin `clawhub/content-rights` page into the "Content Rights Requests" subsection. Moderation states / account standing and ClawHub-itself vulnerabilities are governed by separate pages and are linked, not restated here.

## The core argument: behavior and context, not topic, decide

The policy's central claim is that **context matters** more than subject. The same topic can be acceptable in a narrow defensive or consent-based setting and unacceptable when packaged as an abuse workflow — so a listing is judged by what it does, what it asks users to run, how it represents itself, and how it is published, rather than by its category label alone. This framing is why "Defensive security, moderation, and abuse review" content is *allowed* (when framed for authorized review, preserving evidence, with clear human-approval boundaries) while the same capabilities packaged as an abuse workflow are *disallowed*. The policy applies symmetrically to listing content and to publisher conduct.

## Allowed content

ClawHub welcomes content that is useful, understandable, and published in good faith. The source defines five allowed categories, each gated by an "Allowed when" condition (verbatim conditions):

- **Developer productivity** — allowed when the listing helps users build, test, migrate, debug, document, or operate software.
- **UI, data, and automation workflows** — allowed when the scope is clear, required credentials are explicit, and risky actions include review, dry-run, preview, or confirmation paths.
- **Defensive security, moderation, and abuse review** — allowed when the tool is framed for authorized review, preserves evidence, and keeps human approval boundaries clear.
- **Personal or team workflows** — allowed when the workflow uses consent-based accounts, transparent setup, and explicit permissions.
- **Maintained catalogs** — allowed when each listing is distinct, useful, accurately described, and reasonably maintained.

## Disallowed content

ClawHub does not host content whose main purpose is abuse, deception, unsafe execution, or rights infringement. The source enumerates seven disallowed-content categories (each is a "Not allowed" row):

- **Unauthorized access or security bypass** — auth bypass, account takeover, rate-limit abuse, live call or agent takeover, reusable session theft, or auto-approving pairing flows for unapproved users.
- **Platform abuse and ban evasion** — stealth accounts after bans, account warming or farming, fake engagement, multi-account automation, mass posting, spam bots, or automation built to avoid detection.
- **Fraud, scams, and deceptive financial workflows** — fake certificates or invoices, deceptive payment flows, scam outreach, fake social proof, synthetic-identity workflows for fraud, or spending/charging tools without clear human approval.
- **Privacy-invasive enrichment or surveillance** — contact scraping for spam, doxxing, stalking, lead extraction paired with unsolicited outreach, covert monitoring, non-consensual biometric matching, or use of leaked data or breach dumps.
- **Non-consensual impersonation or identity manipulation** — face swap, digital twins, cloned influencers, fake personas, or other tooling used to impersonate or mislead.
- **Explicit sexual content or safety-disabled adult generation** — NSFW image, video, or content generation; adult-content wrappers around third-party APIs; or listings whose primary purpose is explicit sexual content.
- **Hidden, unsafe, or misleading execution requirements** — obfuscated install commands, pipe-to-shell installers such as downloaded content run with `sh` or `bash` without clear reviewability, undeclared secret or private-key requirements, remote `npx @latest` execution without clear reviewability, or metadata that hides what the listing really needs to run.
- **Copyright-infringing or rights-violating material** — republishing someone else's skill, plugin, docs, brand assets, or proprietary code without permission; violating license terms; or impersonating the original author or publisher.

## Disallowed marketplace behavior

Beyond listing content, ClawHub reviews **how publishers use the marketplace**: publishers must not use ClawHub to manipulate discovery, metrics, trust signals, moderation systems, or user attention. The source lists disallowed marketplace behavior as:

- bulk publishing large numbers of low-effort, duplicative, placeholder, or machine-generated listings that do not appear to have real user value
- flooding search or category surfaces with near-identical skills or plugins
- publishing hundreds of listings with little or no usage, maintenance, source clarity, or meaningful differentiation
- artificially inflating installs, downloads, stars, or other engagement metrics through automation, self-install loops, fake accounts, coordinated activity, paid engagement, or other non-organic behavior
- creating or rotating accounts to evade moderation, bans, publisher limits, or marketplace review
- misleading users about ownership, source, capabilities, security posture, install requirements, or affiliation with another project or publisher
- repeatedly uploading content that has already been hidden, removed, or blocked without fixing the underlying issue

The policy is explicit that **high-volume publishing is not automatically abuse**: large catalogs are acceptable when the listings are meaningfully different, accurately described, maintained, and used by real users. Large catalogs become a trust-and-safety problem only when volume is paired with thin, duplicative, misleading, unmaintained, or artificially promoted listings.

## Content rights

If you believe content on ClawHub infringes your copyright or other rights, the policy directs you to the **Content Rights Requests** flow (below) rather than the normal marketplace reporting flow. Do not use normal marketplace reports for copyright or rights claims unless the listing is also unsafe, malicious, or misleading — in which case the standard reporting path applies in addition.

### Content Rights Requests (folded from `clawhub/content-rights`)

If you believe content published on ClawHub infringes your copyright or other rights, submit a **ClawHub Content Rights Request** at `https://forms.openclaw.ai/clawhub-content-rights`. The request should include:

- one or more exact `https://clawhub.ai/<owner>/<skill>` URLs
- your name, organization, and contact email
- a brief explanation of the rights concern
- supporting evidence, if available

ClawHub staff **review requests manually** and may contact the requester or publisher for more information. Depending on the circumstances, affected content may be hidden, restored, or left unchanged. For unsafe marketplace content that is *not* a content-rights concern, the normal reporting flow (Moderation and Account Safety) applies; vulnerabilities in ClawHub itself go to the ClawHub Security page.

## Review and enforcement

ClawHub may use **automated checks, statistical abuse signals, user reports, and staff review** to identify unsafe content or abusive publishing behavior. A key argument here: a signal does not prove abuse by itself; it helps ClawHub decide what needs review. The enforcement actions ClawHub reserves are:

- hide, hold, remove, soft-delete, or — where supported for the resource type — hard-delete violating listings
- block downloads or installs for unsafe releases
- revoke API tokens
- soft-delete associated content
- restrict publishing access
- ban repeat or severe offenders

The policy explicitly **does not guarantee warning-first enforcement for obvious abuse**. Reports, moderation holds, hidden listings, bans, and account standing are detailed on the separate Moderation and Account Safety page.

