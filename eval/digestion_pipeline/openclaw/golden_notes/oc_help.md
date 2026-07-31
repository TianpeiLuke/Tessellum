---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - troubleshooting
keywords:
  - openclaw help hub
  - get unstuck path
  - troubleshooting decision tree
  - install sanity checks
  - openclaw faq first-run models
  - diagnostics environment variables flags
  - gateway troubleshooting doctor
  - openclaw testing suites
topics:
  - OpenClaw
  - Help
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/help
access_control_group: ["general"]
---

# OpenClaw — The Help Hub (Get-Unstuck Index)

## Overview

This note covers the OpenClaw **Help** page (`/help`), the symptom-first "get unstuck" navigation hub that points an operator to the fastest path to a fix when something breaks. It is a pure index page: it carries no procedure of its own, only a curated set of links into the troubleshooting, debugging, install-sanity, gateway-troubleshooting, doctor, FAQ, diagnostics, testing, and community/meta pages. This mirrors the `help` source page in full — its intro "get unstuck" list plus the four H2 sections (FAQ, Diagnostics, Testing, Community and meta). The page's own framing: it is the entry point both for newcomers who want a "what do I click/run" guide and for operators who want the fastest path to a fix.

## Quick "Get Unstuck" Path

The intro section is a flat list of the five most common starting points for the most common problems, in priority order:

- **Troubleshooting** (`/help/troubleshooting`) — a symptom-first decision tree.
- **Debugging** (`/help/debugging`) — watch mode, raw streams, and the dev profile.
- **Install sanity** (`/install/node#troubleshooting`) — Node / npm / PATH checks.
- **Gateway troubleshooting** (`/gateway/troubleshooting`) — gateway-specific issues.
- **Doctor** (`/gateway/doctor`) — automated repair plus a diagnostic bundle.

## FAQ

The FAQ cluster groups three audience-scoped question sets:

- **FAQ** (`/help/faq`) — day-to-day concepts and operational questions.
- **First-run FAQ** (`/help/faq-first-run`) — install, onboard, auth, subscriptions, and early failures.
- **Models FAQ** (`/help/faq-models`) — model selection, failover, and auth profiles.

## Diagnostics

The Diagnostics cluster points to the lower-level inspection surfaces for when a behavior needs to be traced to a cause:

- **Environment variables** (`/help/environment`) — where OpenClaw loads env vars and their precedence.
- **Diagnostics flags** (`/diagnostics/flags`) — runtime diagnostics and verbose modes.
- **Node + tsx crash** (`/debug/node-issue`) — specific Node / tsx runtime crash scenarios.

## Testing

The Testing cluster links the validation surfaces used to confirm a build, update, or plugin install is healthy:

- **Testing** (`/help/testing`) — test suites and Docker runners.
- **Update and plugin tests** (`/help/testing-updates-plugins`) — package update, migration, and plugin install validation.
- **Live tests** (`/help/testing-live`) — network-touching provider and CLI smokes.

## Community and Meta

The Community and meta cluster covers narrative and documentation-structure references rather than fixes:

- **OpenClaw lore** (`/start/lore`) — the story.
- **Docs hubs** (`/start/hubs`) — how this documentation is organized.
- **Docs directory** (`/start/docs-directory`) — the full file map.

**Source**: OpenClaw documentation — `help` (mirror `inbox/openclaw_docs/help.md`)
**Last Updated**: 2026-06-22
**Status**: Active
