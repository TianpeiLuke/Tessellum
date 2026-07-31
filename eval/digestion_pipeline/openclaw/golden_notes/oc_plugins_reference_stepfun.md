---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw stepfun plugin
  - stepfun provider
  - stepfun-plan provider
  - "@openclaw/stepfun-provider"
  - clawhub stepfun provider
  - openclaw model provider plugin
  - providers surface stepfun
  - npm clawhub install route
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/stepfun
access_control_group: ["general"]
---

# OpenClaw — StepFun Provider Plugin Reference

## Overview

This note is the install/configure/audit reference card for the OpenClaw **StepFun plugin**, mirroring the `plugins/reference/stepfun` source page. The plugin adds StepFun and StepFun Plan model-provider support to OpenClaw — it is a model-provider plugin whose **Surface** contributes the `stepfun` and `stepfun-plan` provider IDs. It ships as the npm package `@openclaw/stepfun-provider` and is installable via npm or via ClawHub (`clawhub:@openclaw/stepfun-provider`). The deep conceptual provider-setup guide lives at `/providers/stepfun` (linked, not duplicated here); this card carries only the three operational facts the source page states — Distribution, Surface, and the Related-docs pointer.

## Distribution

- **Package:** `@openclaw/stepfun-provider`
- **Install route:** npm; ClawHub: `clawhub:@openclaw/stepfun-provider`

The package is published under the `@openclaw/` npm scope and can be installed either from npm directly or through ClawHub (the OpenClaw plugin registry) using the ClawHub reference `clawhub:@openclaw/stepfun-provider`. The source page does not state any additional install flags, environment variables, or defaults beyond the package name and these two install routes.

## Surface

`providers: stepfun, stepfun-plan`

The plugin contributes a `providers:` surface (the capability category a model-provider plugin adds to OpenClaw). It registers two provider IDs — `stepfun` and `stepfun-plan` — making StepFun and StepFun Plan models selectable in OpenClaw's model catalog and routable through the provider chain. The source page lists only these two surface IDs and no per-model or auth detail.

**Source**: OpenClaw documentation — `plugins/reference/stepfun` (mirror `inbox/openclaw_docs/plugins/reference/stepfun.md`)
**Last Updated**: 2026-06-22
**Status**: Active
