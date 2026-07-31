---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - diagnostics
keywords:
  - openclaw diagnostics-otel plugin
  - opentelemetry exporter
  - "@openclaw/diagnostics-otel"
  - otel metrics traces logs
  - clawhub plugin install
  - diagnostics exporter surface
  - agent runtime observability
topics:
  - OpenClaw
  - Plugins Reference
  - Observability
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/diagnostics-otel
access_control_group: ["general"]
---

# OpenClaw — Diagnostics OpenTelemetry Plugin (`@openclaw/diagnostics-otel`)

## Overview

This note is the reference card for the OpenClaw **Diagnostics OpenTelemetry plugin**, mirroring the `plugins/reference/diagnostics-otel` source page. The plugin is described in source as an "OpenClaw diagnostics OpenTelemetry exporter for metrics, traces, and logs" — an OpenTelemetry (OTel) exporter that ships OpenClaw runtime telemetry to an OTel backend. The card documents two things only: the plugin's **Distribution** (its npm package name and ClawHub install route) and its plugin **Surface**. The full gateway-side OTel configuration is not described here; it lives in the separate gateway OpenTelemetry doc, which this card points at. The source page is read-when guidance: it is intended for builders installing, configuring, or auditing the `diagnostics-otel` plugin.

## Distribution

The plugin is published as the npm package **`@openclaw/diagnostics-otel`**. Per source, the install route is **npm**, and the ClawHub install reference is **`clawhub:@openclaw/diagnostics-otel`**. No version pin, configuration keys, defaults, or environment variables are listed on the source page (those belong to the full gateway OpenTelemetry configuration doc, not this reference card).

## Surface

The source page declares the plugin's surface as a single entry: **`plugin`**. In the OpenClaw plugins-reference vocabulary, the `## Surface` section enumerates the contract/channel/skill surfaces a plugin provides; for `diagnostics-otel` that surface is the generic `plugin` entry — it registers as an OpenClaw plugin rather than declaring a more specific contract ID (such as `tools`, `channels`, or a named provider contract). As a diagnostics exporter, it observes OpenClaw runtime events and forwards the three OpenTelemetry signal types named in the summary — metrics, traces, and logs — to an OTel collector. The source page does not enumerate individual exported signals, metric names, or trace spans beyond that summary.

**Source**: OpenClaw documentation — `plugins/reference/diagnostics-otel` (mirror `inbox/openclaw_docs/plugins/reference/diagnostics-otel.md`)
**Last Updated**: 2026-06-22
**Status**: Active
