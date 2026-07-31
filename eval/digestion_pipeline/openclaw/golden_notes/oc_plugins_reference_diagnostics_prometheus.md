---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - diagnostics
keywords:
  - openclaw diagnostics prometheus plugin
  - prometheus exporter runtime metrics
  - "@openclaw/diagnostics-prometheus"
  - clawhub diagnostics prometheus
  - prometheus scrape endpoint
  - plugin surface
  - openclaw runtime metrics
topics:
  - OpenClaw
  - Plugins
  - Diagnostics
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/diagnostics-prometheus
access_control_group: ["general"]
---

# OpenClaw — Diagnostics Prometheus Plugin (`@openclaw/diagnostics-prometheus`)

## Overview

This note is the reference card for the OpenClaw **diagnostics Prometheus plugin**: a Prometheus exporter for OpenClaw runtime metrics. It mirrors the `plugins/reference/diagnostics-prometheus` source page — a stub-class reference card whose load-bearing facts are the npm package name, the install route (npm plus ClawHub), and the plugin surface. The full gateway-side Prometheus configuration is documented separately under `gateway/prometheus`; this card is the per-plugin identity entry in the OpenClaw plugins catalog.

## Distribution

- **Package**: `@openclaw/diagnostics-prometheus`
- **Install route**: npm; ClawHub: `clawhub:@openclaw/diagnostics-prometheus`

The plugin is distributed as a standalone npm package and is also installable through ClawHub via the route `clawhub:@openclaw/diagnostics-prometheus`. The source page does not specify a default-on/bundled status, configuration keys, or a scrape port/path for this card — those details are not specified in source here and live in the full gateway Prometheus configuration doc.

## Surface

The plugin's declared surface is: `plugin`.

The source page lists the surface as `plugin` — i.e., the package registers as an OpenClaw plugin (rather than declaring a more specific contract such as `tools`, `channels`, or `webSearchProviders` on this card). Functionally it is a diagnostics exporter: it exposes OpenClaw runtime metrics so a Prometheus server can pull (scrape) them, the pull/scrape counterpart to the push/OTLP model of the sibling `@openclaw/diagnostics-otel` exporter.

**Source**: OpenClaw documentation — `plugins/reference/diagnostics-prometheus` (mirror `inbox/openclaw_docs/plugins/reference/diagnostics-prometheus.md`)
**Last Updated**: 2026-06-22
**Status**: Active
