---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw pixverse plugin
  - pixverse-provider plugin
  - pixverse video generation provider
  - videoGenerationProviders contract
  - text-to-video image-to-video
  - clawhub pixverse install
  - openclaw media provider plugin
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/reference/pixverse
access_control_group: ["general"]
---

# OpenClaw — PixVerse Plugin Reference Card

## Overview

This note models the OpenClaw **PixVerse plugin** as a plugin-manifest reference card, mirroring the `plugins/reference/pixverse` source page. The page's one-line summary is "OpenClaw PixVerse video generation provider plugin," and its `read_when` trigger is "You are installing, configuring, or auditing the pixverse plugin." The card carries the plugin's identity — its npm package name, its install route, and its Surface declaration (the typed media-generation contract it contributes) — plus a `Related docs` pointer to the matching `/providers/pixverse` user page. This is a leaf reference record (model BB), not a how-to procedure: the underlying API key/env setup, supported modes/models, provider options, and configuration keys live on the linked `/providers/pixverse` provider page, not inline here.

## Distribution

The PixVerse plugin's package identity and install route, reproduced verbatim from the source page:

- Package: `@openclaw/pixverse-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/pixverse-provider`

Unlike a bundled plugin (one whose install route reads "included in OpenClaw"), PixVerse is an **installed plugin** distributed separately — its install route names both npm and the ClawHub package identifier `clawhub:@openclaw/pixverse-provider`, so an operator adds it explicitly rather than receiving it pre-shipped with the gateway. The card declares no additional install flags, version pins, or onboarding steps; those belong to the `/providers/pixverse` user page.

## Surface

The Surface declaration is the load-bearing, machine-meaningful content of the card — the typed contract the plugin registers with the OpenClaw extension framework. Reproduced verbatim from the source page:

> contracts: videoGenerationProviders

So the PixVerse plugin contributes a single media-generation contract: `videoGenerationProviders` (video generation). Through this contract, PixVerse's hosted text-to-video and image-to-video models become selectable in OpenClaw's shared video-generation surface. The card's Surface block names only the contract (it does not separately list a `providers:` entry, unlike some sibling cards); the provider id, supported models, modes, and configuration keys are documented on the linked `/providers/pixverse` page rather than on this reference card. This card states no further environment variables, model identifiers, or option bags.

**Source**: OpenClaw documentation — `plugins/reference/pixverse` (mirror `inbox/openclaw_docs/plugins/reference/pixverse.md`)
**Last Updated**: 2026-06-22
**Status**: Active
