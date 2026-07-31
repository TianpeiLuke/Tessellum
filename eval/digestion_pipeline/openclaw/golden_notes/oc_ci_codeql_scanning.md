---
tags:
  - resource
  - documentation
  - openclaw
  - ci
  - codeql
keywords:
  - openclaw codeql scanning
  - narrow first-pass security scanner
  - codeql security categories
  - critical quality non-security shard
  - quality separate from security signal
  - codeql android macos security shards
  - high critical security-severity filter
  - codeql pr guard
topics:
  - OpenClaw
  - CI
  - CodeQL Security Scanning
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/ci
access_control_group: ["general"]
---

# OpenClaw — CodeQL: Narrow Security Scanning, Quality Kept Separate

## Overview

This note presents the **argument** behind OpenClaw's CodeQL strategy as documented in the `## CodeQL` section of the `ci` source page: rather than running a full repository sweep, OpenClaw deliberately treats CodeQL as a **narrow first-pass security scanner** over the highest-risk JavaScript/TypeScript surfaces, and pairs it with a deliberately *separate* `CodeQL Critical Quality` non-security shard. The claim being defended is that scoping the security scan tightly (high-confidence queries, high/critical `security-severity` only, a small set of boundary categories) and isolating quality findings from security findings produces a more actionable, less noisy security signal than a broad scan would. This note covers the security category map, the Android/macOS platform-specific security shards, the PR-guard scoping rationale, the Critical Quality category map, and the explicit "quality stays separate from security" justification — all mirroring `inbox/openclaw_docs/ci.md`.

## The Core Argument: A Narrow First-Pass Scanner, Not a Full Sweep

The `CodeQL` workflow is "intentionally a narrow first-pass security scanner, not the full repository sweep." Daily, manual, and non-draft pull request guard runs scan Actions workflow code plus the highest-risk JavaScript/TypeScript surfaces with high-confidence security queries filtered to high/critical `security-severity`. The deliberate choices in that sentence are the argument: (1) only the *highest-risk* JS/TS surfaces are in scope, (2) only *high-confidence* security queries run, and (3) results are filtered to *high/critical* severity. Each narrowing decision trades breadth for signal — the page's position is that a focused security scan that engineers act on beats an exhaustive scan whose findings are ignored.

The pull request guard reinforces this by staying light: it only starts for changes under `.github/actions`, `.github/codeql`, `.github/workflows`, `packages`, or `src`, and it runs the same high-confidence security matrix as the scheduled workflow. Android and macOS CodeQL stay out of PR defaults. The justification is cost-vs-risk balance: the PR-time guard gates the highest-risk change paths without making every PR wait behind expensive platform builds, while the scheduled cadence still covers the platform surfaces.

## Security Categories

The security scan is decomposed into five high-confidence boundary categories, each mapped to a defined high-risk surface (verbatim from source):

| Category | Surface |
| --- | --- |
| `/codeql-security-high/core-auth-secrets` | Auth, secrets, sandbox, cron, and gateway baseline |
| `/codeql-security-high/channel-runtime-boundary` | Core channel implementation contracts plus the channel plugin runtime, gateway, Plugin SDK, secrets, audit touchpoints |
| `/codeql-security-high/network-ssrf-boundary` | Core SSRF, IP parsing, network guard, web-fetch, and Plugin SDK SSRF policy surfaces |
| `/codeql-security-high/mcp-process-tool-boundary` | MCP servers, process execution helpers, outbound delivery, and agent tool-execution gates |
| `/codeql-security-high/plugin-trust-boundary` | Plugin install, loader, manifest, registry, package-manager install, source-loading, and Plugin SDK package contract trust surfaces |

These five categories are the concrete embodiment of "highest-risk surfaces": they target the auth/secret/sandbox boundary, the channel runtime, the SSRF/network boundary, the process-exec and tool-execution gates, and the plugin-trust boundary — precisely the surfaces where a security defect would be most damaging. The narrow-scope argument is therefore not arbitrary; the scope is the risk-prioritized boundary map itself.

## Platform-Specific Security Shards

Two platform security shards run on a slower cadence than the JS/TS defaults, which is itself part of the cost argument — they are kept out of daily defaults because the platform build dominates runtime:

- `CodeQL Android Critical Security` — scheduled Android security shard. Builds the Android app manually for CodeQL on the smallest Blacksmith Linux runner accepted by workflow sanity. Uploads under `/codeql-critical-security/android`.
- `CodeQL macOS Critical Security` — weekly/manual macOS security shard. Builds the macOS app manually for CodeQL on Blacksmith macOS, filters dependency build results out of uploaded SARIF, and uploads under `/codeql-critical-security/macos`. Kept outside daily defaults because macOS build dominates runtime even when clean.

The explicit reasoning ("Kept outside daily defaults because macOS build dominates runtime even when clean") is the page defending the scheduling decision: the security value of the platform shards does not justify paying their build cost on every run, so they are placed on a scheduled/weekly/manual cadence instead.

## Critical Quality: A Deliberately Separate, Non-Security Shard

`CodeQL Critical Quality` is the matching non-security shard. It runs only error-severity, non-security JavaScript/TypeScript quality queries over narrow high-value surfaces on the smaller Blacksmith Linux runner. Its existence as a *separate* workflow — rather than folding quality queries into the security scan — is the second half of the argument.

The PR guard for the quality shard is intentionally smaller than the scheduled profile: non-draft PRs only run the matching `agent-runtime-boundary`, `config-boundary`, `core-auth-secrets`, `channel-runtime-boundary`, `gateway-runtime-boundary`, `memory-runtime-boundary`, `mcp-process-runtime-boundary`, `provider-runtime-boundary`, `session-diagnostics-boundary`, `plugin-boundary`, `plugin-sdk-package-contract`, and `plugin-sdk-reply-runtime` shards for the corresponding agent-command/model/tool-execution, config schema/migration/IO, auth/secrets/sandbox, channel-runtime, gateway-protocol, memory-runtime, MCP/process, provider-runtime, session-diagnostics, plugin-loader, Plugin SDK/package-contract, or Plugin SDK reply-runtime changes. CodeQL config and quality workflow changes run all twelve PR quality shards.

Manual dispatch accepts a profile selector for running one quality shard in isolation:

```
profile=all|agent-runtime-boundary|config-boundary|core-auth-secrets|channel-runtime-boundary|gateway-runtime-boundary|memory-runtime-boundary|mcp-process-runtime-boundary|plugin-boundary|plugin-sdk-package-contract|plugin-sdk-reply-runtime|provider-runtime-boundary|session-diagnostics-boundary
```

The narrow profiles are "teaching/iteration hooks for running one quality shard in isolation." The Critical Quality category map (verbatim):

| Category | Surface |
| --- | --- |
| `/codeql-critical-quality/core-auth-secrets` | Auth, secrets, sandbox, cron, and gateway security boundary code |
| `/codeql-critical-quality/config-boundary` | Config schema, migration, normalization, and IO contracts |
| `/codeql-critical-quality/gateway-runtime-boundary` | Gateway protocol schemas and server method contracts |
| `/codeql-critical-quality/channel-runtime-boundary` | Core channel and bundled channel plugin implementation contracts |
| `/codeql-critical-quality/agent-runtime-boundary` | Command execution, model/provider dispatch, auto-reply dispatch and queues, and ACP control-plane runtime contracts |
| `/codeql-critical-quality/mcp-process-runtime-boundary` | MCP servers and tool bridges, process supervision helpers, and outbound delivery contracts |
| `/codeql-critical-quality/memory-runtime-boundary` | Memory host SDK, memory runtime facades, memory Plugin SDK aliases, memory runtime activation glue, and memory doctor commands |
| `/codeql-critical-quality/session-diagnostics-boundary` | Reply queue internals, session delivery queues, outbound session binding/delivery helpers, diagnostic event/log bundle surfaces, and session doctor CLI contracts |
| `/codeql-critical-quality/plugin-sdk-reply-runtime` | Plugin SDK inbound reply dispatch, reply payload/chunking/runtime helpers, channel reply options, delivery queues, and session/thread binding helpers |
| `/codeql-critical-quality/provider-runtime-boundary` | Model catalog normalization, provider auth and discovery, provider runtime registration, provider defaults/catalogs, and web/search/fetch/embedding registries |
| `/codeql-critical-quality/ui-control-plane` | Control UI bootstrap, local persistence, gateway control flows, and task control-plane runtime contracts |
| `/codeql-critical-quality/web-media-runtime-boundary` | Core web fetch/search, media IO, media understanding, image-generation, and media-generation runtime contracts |
| `/codeql-critical-quality/plugin-boundary` | Loader, registry, public-surface, and Plugin SDK entrypoint contracts |
| `/codeql-critical-quality/plugin-sdk-package-contract` | Published package-side Plugin SDK source and plugin package contract helpers |

## Why Quality Is Kept Separate From Security Signal

The decisive justification is stated directly in source: "Quality stays separate from security so quality findings can be scheduled, measured, disabled, or expanded without obscuring security signal." This is the load-bearing argument of the whole section — mixing non-security quality queries into the security scan would dilute the high/critical security signal that engineers must act on, whereas a separate shard lets quality coverage be tuned (scheduled, measured, disabled, or expanded) independently without polluting the security results. The page also bounds future expansion on the same principle: "Swift, Python, and bundled-plugin CodeQL expansion should be added back as scoped or sharded follow-up work only after the narrow profiles have stable runtime and signal." In other words, breadth is earned — it is added only once the narrow profiles have proven stable runtime and signal, never as an upfront full sweep.

**Source**: OpenClaw documentation — `ci` (mirror `inbox/openclaw_docs/ci.md`, `## CodeQL` section)
**Last Updated**: 2026-06-22
**Status**: Active
