---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - security
keywords:
  - clawhub security reporting
  - github security advisories openclaw/clawhub
  - vulnerability disclosure policy
  - platform bug vs third-party skill plugin
  - registry publishing integrity bugs
  - hosted-service vulnerability disclosure
  - user-installed artifact disclosure
  - real user impact threshold
topics:
  - OpenClaw
  - ClawHub Security
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/clawhub/security
access_control_group: ["general"]
---

# OpenClaw — ClawHub Security Reporting and Disclosure Policy

## Overview

This note states the ClawHub security-reporting and vulnerability-disclosure policy from the `clawhub/security` source page: it argues which bugs belong in a ClawHub security report versus which should go to a third-party publisher, and it argues when a ClawHub vulnerability is publicly disclosed versus held private. ClawHub is OpenClaw's open-source skill and plugin registry; this is the page a reporter or installer reads to know where to file an issue and what disclosure to expect. The page has three parts — the report-routing intro, the "Vulnerability disclosure" section, and a "Related pages" cross-link block — all of which this note covers.

## Where to report: ClawHub platform bugs, not third-party artifact code

The page's first claim is a routing rule: ClawHub security issues can be reported through **GitHub Security Advisories for `openclaw/clawhub`**. GitHub Security Advisories are the channel for vulnerabilities **in ClawHub itself**. The page enumerates the bug classes that make a good ClawHub advisory report — vulnerabilities in:

- the ClawHub website, API, or CLI
- registry publishing, downloads, installs, or artifact integrity
- authentication, authorization, or API tokens
- scanning, moderation, or report handling

The contrasting argument bounds that scope: you must **not** use ClawHub advisories for vulnerabilities in a **third-party skill or plugin's own source code**. Those are reported directly to the publisher or to the source repository linked from the ClawHub listing. The load-bearing distinction is platform-vs-artifact: the registry's own surfaces (hosting, publishing pipeline, integrity, authn/authz, scanning, moderation) are ClawHub's responsibility and its advisory scope, whereas the code inside a published skill or plugin is the publisher's responsibility and is reported to them, not to ClawHub.

## Vulnerability disclosure: hosted-service default-private vs user-installed always-public

The "Vulnerability disclosure" section argues for two different disclosure regimes, split by whether users must take action.

Because ClawHub is a **hosted cloud application**, ClawHub **service** vulnerabilities are **not publicly disclosed by default**. The reasoning is that a server-side fix to a hosted service can be applied centrally without users doing anything, so default-private disclosure does not leave users exposed. The exception — the threshold that flips a hosted-service vulnerability to public — is **evidence of real user impact or that users need to take action**. The page gives concrete examples of "real user impact": confirmed exploitation, exposure of user data or secrets, malicious content reaching users because of a platform failure, or any issue that requires users to rotate credentials, update local software, or take other protective action.

By contrast, vulnerabilities in **user-installed software are publicly disclosed** — such as ClawHub CLI packages, binaries, libraries, or other release artifacts that users need to update locally. The argument here is symmetric to the hosted case: an artifact running on a user's machine cannot be fixed centrally, so the user must learn of the issue and update it themselves, which makes public disclosure necessary rather than optional. The governing principle across both regimes is whether a user must act: if a central server-side fix suffices, the hosted-service vulnerability can stay private; if the user must update a local artifact, rotate a credential, or otherwise protect themselves, the vulnerability is disclosed.

**Source**: OpenClaw documentation — `clawhub/security` (mirror `inbox/openclaw_docs/clawhub/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
