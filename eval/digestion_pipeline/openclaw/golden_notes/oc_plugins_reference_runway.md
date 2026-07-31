---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw runway plugin
  - runway-provider plugin
  - runway video generation provider
  - videoGenerationProviders contract
  - included in openclaw bundled plugin
  - openclaw media provider plugin
  - plugin reference card distribution surface
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/runway
access_control_group: ["general"]
---

# OpenClaw — Runway Plugin Reference Card

## Overview

This note models the OpenClaw **Runway plugin** as a plugin-manifest reference card, mirroring the `plugins/reference/runway` source page. The page's one-line summary is "Adds video generation provider support," and its `read_when` trigger is "You are installing, configuring, or auditing the runway plugin." The card carries the plugin's identity — its npm-style package name, its install route, and its Surface declaration (the typed media-generation contract it contributes) — plus a `Related docs` pointer to the matching `/providers/runway` user page. This is a leaf reference record (model BB), not a how-to procedure: the underlying API key/env setup, supported models, modes, provider options, and configuration keys live on the linked `/providers/runway` provider page, not inline here.

## Distribution

The Runway plugin's package identity and install route, reproduced verbatim from the source page:

- Package: `@openclaw/runway-provider`
- Install route: included in OpenClaw

The install route reads "included in OpenClaw," which marks Runway as a **bundled plugin** — one that ships pre-installed with the gateway rather than being added separately by an operator. This is the explicit contrast to an installed plugin (whose route would name npm and a `clawhub:` package identifier): a bundled plugin's `@openclaw/runway-provider` package is loaded at gateway startup with no extra install step, version pin, or ClawHub fetch. The card declares no additional install flags or onboarding steps; those belong to the `/providers/runway` user page.

## Surface

The Surface declaration is the load-bearing, machine-meaningful content of the card — the typed contract the plugin registers with the OpenClaw extension framework. Reproduced verbatim from the source page:

> contracts: videoGenerationProviders

So the Runway plugin contributes a single media-generation contract: `videoGenerationProviders` (video generation). Through this contract, Runway's hosted video-generation models become selectable in OpenClaw's shared video-generation surface, where they back the agent's video-generation tool. The card's Surface block names only the `contracts:` entry; it does not separately list a `providers:` id. The provider id, supported models, modes, and configuration keys are documented on the linked `/providers/runway` page rather than on this reference card. This card states no further environment variables, model identifiers, or option bags.

**Source**: OpenClaw documentation — `plugins/reference/runway` (mirror `inbox/openclaw_docs/plugins/reference/runway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
