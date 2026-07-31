---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - namespace_claims
keywords:
  - clawhub namespace claim
  - org namespace ownership dispute
  - package scope claim
  - owner handle skill slug claim
  - org-namespace-claim issue form
  - namespace reserve transfer rename
  - clawhub publishing ownership
topics:
  - OpenClaw
  - ClawHub Namespace Claims
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/namespace-claims
access_control_group: ["general"]
---

# OpenClaw — Filing a ClawHub Org / Namespace Claim

## Overview

This note is the procedure for requesting ClawHub staff review of an ownership dispute over a public ClawHub namespace, mirroring the `clawhub/namespace-claims` source page. ClawHub uses owner handles, org handles, skill slugs, plugin package names, and package scopes as public namespaces. When a namespace appears to belong to a real-world project, brand, package ecosystem, or organization but is already claimed, reserved, misleading, or disputed on ClawHub, you ask staff to review it via the [Org / Namespace Claim issue form](https://github.com/openclaw/clawhub/issues/new?template=org-namespace-claim.yml). This path is for public, non-sensitive ownership review only: do NOT use in-product reports or the account appeal form for namespace claims. The note walks through when a claim is the right tool, what to confirm before filing, what public evidence to include, what secrets to keep out, and the possible staff outcomes.

## When to Open a Claim

Open a namespace claim when you believe ClawHub staff should review whether a namespace should be reserved, transferred, renamed, hidden, quarantined, aliased, or otherwise changed because of real-world ownership. Examples that warrant a claim:

- an org handle that matches your GitHub org, project, company, or community;
- a package scope such as `@example-org/*` that should only publish under the matching ClawHub owner;
- a skill slug or plugin package name that appears to impersonate a project;
- a brand, trademark, project rename, or package history dispute;
- a deleted, inactive, or unreachable owner that blocks the rightful namespace owner.

If the listing is unsafe, malicious, or misleading beyond the ownership dispute, also follow the relevant moderation or security guidance — the namespace claim form is for ownership review, NOT emergency vulnerability disclosure.

## Before You File

First confirm that you are publishing with the owner that matches the namespace. For plugin packages, scoped names such as `@example-org/example-plugin` must be published as the matching `example-org` owner. If you can manage the current owner, fix the namespace directly by publishing, renaming, transferring, hiding, or deleting the affected resource yourself. Use a claim only when you cannot manage the current owner, or when staff needs to resolve a dispute between parties.

## Evidence to Include

Use public, non-sensitive evidence. Helpful proof includes:

- GitHub org, repo, release, or maintainer history;
- official project docs that name the namespace;
- domain or official email-domain proof;
- npm, PyPI, crates.io, or other package-registry scope control;
- trademark, brand, or project ownership evidence that is safe to discuss publicly;
- source repository history, package history, or public rename notices;
- links to the disputed ClawHub owner, skill, plugin, package, or issue.

Explain what each link proves. Staff should be able to understand the relationship without needing private credentials or secrets.

## What Not to Include

Do not put secrets or private proof in a public GitHub issue. Specifically, do not include:

- API tokens, signing keys, or credentials;
- DNS challenge tokens;
- private legal files or contracts;
- personal identity documents;
- private emails, private security reports, or confidential customer data.

The claim form asks whether sensitive evidence needs a private staff channel. Use that option instead of posting sensitive material publicly.

## Possible Outcomes

Depending on the evidence and risk, ClawHub staff may reserve a namespace, transfer ownership, rename a resource, hide or quarantine an existing listing, add an alias or redirect, ask for more proof, or decline the request. Namespace review does not guarantee that every matching name will be transferred: staff weighs public evidence, existing usage, security risk, and user impact before acting.

**Source**: OpenClaw documentation — `clawhub/namespace-claims` (mirror `inbox/openclaw_docs/clawhub/namespace-claims.md`)
**Last Updated**: 2026-06-22
**Status**: Active
