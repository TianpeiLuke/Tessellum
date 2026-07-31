---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw llm-task plugin
  - openclaw lobster plugin
  - contracts tools plugin
  - workflow tool plugin
  - structured task json llm tool
  - typed pipeline resumable approvals
  - openclaw llm-task package
  - openclaw lobster package
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/llm-task
access_control_group: ["general"]
---

# OpenClaw — LLM Task & Lobster Workflow Tool Plugins

## Overview

This note is the install/enable procedure card for the two `l*` workflow / structured-task tool plugins in the OpenClaw plugin reference: **LLM Task** (`@openclaw/llm-task`) and **Lobster** (`@openclaw/lobster`). It consolidates the `plugins/reference/llm-task` and `plugins/reference/lobster` inventory pages of the source docs — each a 51–62-word micro-stub — into one focused procedure for the shared capability cluster: both plugins register the same `contracts: tools` capability surface, so both become workflow-callable agent tools, but they differ in npm package, install route, and use case (LLM Task is a generic JSON-only structured-task tool; Lobster is a typed-pipeline workflow tool with resumable approvals). For each plugin this card gives the npm package name, the install route, and the capability contract it registers; the deeper config/DSL of each tool lives in its own `tools/<name>` deep-dive page (linked under References), not here.

## LLM Task plugin (`@openclaw/llm-task`)

LLM Task is described in source as a "Generic JSON-only LLM tool for structured tasks callable from workflows." It is the plugin you reach for when a workflow step needs a single LLM call to return structured (JSON-only) output — i.e. an LLM task exposed as a callable agent tool — rather than a free-form conversational reply.

**Distribution**

- Package: `@openclaw/llm-task`
- Install route: included in OpenClaw (no separate `npm`/ClawHub install step needed; the package ships with OpenClaw and is enabled rather than fetched).

**Surface**

- `contracts: tools` — LLM Task registers the `tools` capability contract, so once enabled it appears in the agent tool registry and is callable from agent workflows like any other built-in tool. Source states the `tools` contract only; it does not list a `providers:` or `channels:` surface.

The source card is read-when guidance ("You are installing, configuring, or auditing the llm-task plugin") and states no configuration keys, flags, or defaults beyond the package, install route, and `contracts: tools` surface. The plugin's structured-task / JSON-output configuration is documented in the `tools/llm-task` deep-dive (External References), which is owned by a separate sub-plan and is not duplicated here. *(The deep-dive page content is not specified in this inventory card.)*

## Lobster plugin (`@openclaw/lobster`)

Lobster is described in source as a "Lobster workflow tool plugin for typed pipelines and resumable approvals." It is the plugin for building typed, multi-step workflow pipelines whose runs can pause for a human approval and later resume — a workflow/orchestration tool rather than a single-shot LLM call.

**Distribution**

- Package: `@openclaw/lobster`
- Install route: `npm`; ClawHub — unlike LLM Task, Lobster is NOT included in OpenClaw and must be installed from `npm` or fetched from ClawHub before it can be enabled.

**Surface**

- `contracts: tools` — Lobster registers the same `tools` capability contract as LLM Task, so it too lands in the agent tool registry and is callable from agent workflows. Source states the `tools` contract only; no `providers:` or `channels:` surface is listed.

The source card is read-when guidance ("You are installing, configuring, or auditing the lobster plugin") and states no configuration keys, pipeline-DSL syntax, or approval-flow defaults beyond the package, install route, and `contracts: tools` surface. Lobster's typed-pipeline DSL and resumable-approval mechanics are documented in the existing Lobster deep-dive digest (linked under Related Notes) and the `tools/lobster` deep-dive page (External References); this inventory card neither defines the DSL nor duplicates that detail.

## Enable Procedure (shared)

Both plugins register the `contracts: tools` surface, so the high-level enable procedure is the same and differs only in the install step: (1) for LLM Task, no fetch is required because it is included in OpenClaw — enable the `@openclaw/llm-task` plugin; for Lobster, first install `@openclaw/lobster` from `npm` or ClawHub, then enable it. (2) Once enabled, each plugin contributes its `tools` contract to the agent tool registry, after which the tool is callable from agent workflows. The exact enable/config invocation and any per-tool options are governed by the OpenClaw plugin system and each tool's own deep-dive page rather than this inventory card; this card is the package ↔ install-route ↔ `contracts: tools` mapping only.

**Source**: OpenClaw documentation — `plugins/reference/llm-task` + `plugins/reference/lobster` (mirror `inbox/openclaw_docs/plugins/reference/llm-task.md`, `inbox/openclaw_docs/plugins/reference/lobster.md`)
**Last Updated**: 2026-06-22
**Status**: Active
