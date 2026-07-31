---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - policy
keywords:
  - openclaw policy plugin
  - policy-backed doctor checks
  - workspace conformance
  - policy.jsonc
  - posture rules
  - openclaw policy check
  - openclaw policy compare
  - attestation hashes
  - named policy scopes
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/policy
access_control_group: ["general"]
---

# OpenClaw — Policy Plugin (Workspace-Conformance Doctor Checks)

## Overview

This note covers the OpenClaw **Policy plugin** (`@openclaw/policy`), a bundled plugin that "adds policy-backed doctor checks for workspace conformance" — mirroring the `plugins/reference/policy` source page (its Distribution, Surface, the manually authored Behavior block on lines 23–73, and the Related docs link-out). The Policy plugin is a *config-conformance* concept: it compares authored requirements stored in `policy.jsonc` against the OpenClaw settings and governed workspace declarations it observes as evidence, then reports drift as doctor findings — without reading runtime state, credentials, or secret values. This note documents what the plugin governs (the posture rule families), how it surfaces (the `policy.jsonc` requirements model, `openclaw policy check`, `openclaw doctor --lint`, `openclaw policy compare`, attestation hashes), and the named-scope overlay model; the fuller CLI behavior of `openclaw policy check`/`compare` lives in the separate `cli/policy` page that this card links out to.

## Distribution

- Package: `@openclaw/policy`
- Install route: included in OpenClaw

The plugin is **bundled** (the page's install route is "included in OpenClaw"), so no separate npm/ClawHub install is required to obtain the policy doctor checks.

## Surface

The page declares the plugin's contributed surface as a single bare entry: `plugin`. Unlike provider or channel reference cards (which name a `providers` / `channels` / `webSearchProviders` contract), the Policy card contributes a generic **plugin** surface — its concrete contribution is the set of policy-conformance doctor checks described in the Behavior section, wired into the `openclaw doctor` lint path and the dedicated `openclaw policy` CLI subcommands.

## Behavior

The Policy plugin contributes **doctor health checks** for policy-managed OpenClaw settings and governed workspace declarations. Policy currently covers a fixed family of posture areas: channel conformance, governed tool metadata, MCP server posture, model-provider posture, private-network access posture, Gateway exposure posture, agent workspace/tool posture, configured global/per-agent tool posture, configured sandbox runtime posture, ingress/channel access posture, data-handling posture, and OpenClaw config secret provider/auth-profile posture.

### Requirements model — `policy.jsonc`, evidence, findings, attestation

Policy stores **authored requirements** in `policy.jsonc`, observes existing OpenClaw settings and workspace declarations as **evidence**, and reports **drift** through `openclaw policy check` and `openclaw doctor --lint`. A clean policy check emits *policy, evidence, findings, and attestation hashes* that operators can record for audit. This authored-requirement-vs-observed-evidence-with-drift-reporting-and-attestation model is the core concept of the plugin: it is governance-as-config, not runtime enforcement.

`openclaw policy compare --baseline <file>` compares one policy file to another policy file. It is **config-level conformance only**: it uses policy rule metadata to verify that the checked policy is not missing or weaker than the authored baseline, and it does **not** inspect runtime state, credentials, or secret values.

### Tool posture rules

Tool posture rules can require approved profiles, workspace-only filesystem tools, bounded exec security/ask/host settings, disabled elevated mode, exact `alsoAllow` entries, and required tool deny entries. The evidence records additive `alsoAllow` entries because they can widen effective tool posture. These checks observe config conformance only; they do not read runtime approval state or add runtime enforcement.

### Sandbox posture rules

Sandbox posture rules can require approved sandbox modes/backends, deny host container networking, deny container namespace joins, require read-only container mounts, deny container runtime socket mounts and unconfined container profiles, and require sandbox browser CDP source ranges. As with tool posture, these checks observe config conformance only; they do not read runtime approval state, inspect live containers, or add runtime enforcement.

### Data-handling posture rules

Data-handling rules can require sensitive logging redaction, deny telemetry content capture, require session retention maintenance, and deny session transcript memory indexing. These checks observe config conformance only; they do not inspect raw logs, telemetry exports, transcripts, memory files, secrets, or personal data.

### Named policy scopes (`scopes.<scopeName>`)

Named policy scopes under `scopes.<scopeName>` can add **stricter** normal policy sections for the selector they list. `agentIds` supports `tools`, `agents.workspace`, `sandbox`, and `dataHandling.memory`; `channelIds` supports `ingress.channels`. Runtime agent ids that are not explicitly listed in `agents.list[]` are checked against inherited global/default posture rather than silently passing with no evidence. Every scope present in `policy.jsonc` must be valid and enforceable for its selector. Overlay rules are **additional claims**, so they do not weaken top-level policy and can produce their own findings when the same observed config violates both scopes.

> The Policy plugin's authored-requirements + observed-evidence + drift-reporting + attestation-hash model is a reusable policy-as-code governance pattern; per this sub-plan it is described inline here and linked to the existing [Policy](../../term_dictionary/term_policy.md) and [Policy Engine / Governance](../../term_dictionary/term_policy_engine_governance.md) terms rather than promoted to a new term note.

**Source**: OpenClaw documentation — `plugins/reference/policy` (mirror `inbox/openclaw_docs/plugins/reference/policy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
